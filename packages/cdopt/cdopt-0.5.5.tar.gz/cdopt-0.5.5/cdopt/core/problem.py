import numpy as np
from typing import Union, Tuple, List



class problem:
    def __init__(self, manifold, obj_fun, obj_grad=None, obj_hvp=None, beta = 'auto', enable_autodiff: bool = True, backbone = None, enable_jit:bool = True, autobeta_args = {}, Xinit = None, **kwargs):
        '''
        Initialize the problem with the provided manifold and objective function.
        Optionally include gradients and Hessian-vector products for the objective function.
        If not provided, automatic differentiation may be used if enabled.
        '''
        
        self.manifold = manifold
        self.obj_fun = obj_fun 


        # Initialize a point on the manifold using the provided initial point or a default.
        self.Xinit = manifold.Init_point(Xinit = Xinit)
        # Convert the initial point to a NumPy array for further computations.
        self.Xinit_vec_np = manifold.tensor2array(manifold.m2v(self.Xinit))
        
        if enable_autodiff:
            # If gradients or Hessian-vector products are not provided, use automatic differentiation.
            if obj_grad is None   or   obj_hvp is None:
                # Select the appropriate automatic differentiation backbone based on user's inputs or defaults.
                if backbone == None:
                    self.backbone = manifold.backbone
                elif backbone == 'jax':
                    from cdopt.core.backbone_jax import backbone_jax
                    self.backbone = backbone_jax()
                elif backbone == 'autograd':
                    # from core.autodiff_ag import autodiff
                    from cdopt.core.backbone_autograd import backbone_autograd
                    self.backbone = backbone_autograd()
                elif backbone == 'torch':
                    from cdopt.core.backbone_torch import backbone_torch
                    self.backbone = backbone_torch(**kwargs)
                else: 
                    self.backbone = backbone(**kwargs)
                
                autodiff = self.backbone.autodiff

                # Use automatic differentiation to compute gradients and Hessian-vector products if it is not provided.
                    
                if  obj_hvp is None:
                    self.obj_grad, self.obj_hvp = autodiff(obj_fun, obj_grad, manifold.manifold_type)
                else:
                    self.obj_grad,  = autodiff(obj_fun,obj_grad, manifold.manifold_type)
                
            else:
                # Use provided gradients and Hessian-vector products.
                self.obj_grad = obj_grad 
                self.obj_hvp = obj_hvp 


            # Automatically generate the penalty parameter if it is not provided.
            if beta == "auto":
                self.beta = self.generate_penalty_parameter( autobeta_args = autobeta_args )
            else:
                self.beta = beta



            # Generate the constraint dissolving function, together with its gradients and and Hessian-vector products.
            self.cdf_fun = self.manifold.generate_cdf_fun(self.obj_fun, self.beta)
            self.cdf_grad = self.manifold.generate_cdf_grad(self.obj_grad, self.beta)
            self.cdf_hvp = self.manifold.generate_cdf_hess(self.obj_grad, self.obj_hvp, self.beta)

            # If JIT compilation is enabled and a backbone is provided, compile these functions for efficiency.
            # Currently, JIT is only supported for JAX. 
            if enable_jit and (backbone is not None):
                self.cdf_fun = self.backbone.jit(self.cdf_fun)
                self.cdf_grad = self.backbone.jit(self.cdf_grad)
                self.cdf_hvp = self.backbone.jit(self.cdf_hvp)



            # Wrap the constraint dissolving function to work with vector inputs by converting between manifold and vector representations.
            self.cdf_fun_vec = lambda y: self.cdf_fun(self.manifold.v2m(y))
            self.cdf_grad_vec= lambda y: self.manifold.m2v( self.cdf_grad(self.manifold.v2m(y)) )
            self.cdf_hvp_vec = lambda y,p: self.manifold.m2v( self.cdf_hvp(self.manifold.v2m(y), self.manifold.v2m(p)) )


            # Convert the outputs to NumPy arrays for compatibility with numerical libraries.

            # self.cdf_fun_vec_np = lambda y: float(self.manifold.tensor2array(self.cdf_fun_vec( self.manifold.array2tensor(y)) ))
            self.cdf_fun_vec_np = lambda y: float(self.cdf_fun_vec( self.manifold.array2tensor(y)) )
            self.cdf_grad_vec_np = lambda y: self.manifold.tensor2array(self.cdf_grad_vec( self.manifold.array2tensor(y)) )
            self.cdf_hvp_vec_np = lambda y,p: self.manifold.tensor2array(self.cdf_hvp_vec(self.manifold.array2tensor(y), self.manifold.array2tensor(p))   )

        else:

            def _raise_not_implemented_error(*args, **kwargs):
                raise NotImplementedError("Automatical differentiation not enabled")

            # Assign objective function and its derivatives if available; otherwise use the placeholder error function.
            self.obj_fun = obj_fun
            self.obj_grad = obj_grad
            self.obj_hvp = obj_hvp

            self.cdf_fun = self.manifold.generate_cdf_fun(self.obj_fun, self.beta)
            if enable_jit:
                self.cdf_fun = self.backbone.jit(self.cdf_fun)
            
            # Wrap the constraint dissolving function to work with vector inputs.
            self.cdf_fun_vec = lambda y: self.cdf_fun(self.manifold.v2m(y))

            
            # If gradients are provided, generate and possibly compile the geadients of constraint dissolving function.
            if obj_grad is not None:
                self.cdf_grad = self.manifold.generate_cdf_grad(self.obj_grad, self.beta)
                if enable_jit:
                    self.cdf_grad = self.backbone.jit(self.cdf_grad)

                self.cdf_grad_vec = lambda y: self.manifold.m2v( self.cdf_grad(self.manifold.v2m(y)) )

            else:
                self.cdf_grad = _raise_not_implemented_error
                self.cdf_grad_vec= _raise_not_implemented_error


            # If Hessian-vector products are provided, generate and possibly compile the Hessian-vector product of constraint dissolving function.
            if obj_hvp is not None:
                self.cdf_hvp = self.manifold.generate_cdf_hess(self.obj_grad, self.obj_hvp, self.beta)
                if enable_jit:
                    self.cdf_hvp = self.backbone.jit(self.cdf_hvp)

                self.cdf_hvp_vec = lambda y,p: self.manifold.m2v( self.cdf_hvp(self.manifold.v2m(y), self.manifold.v2m(p)) )

            else:
                self.cdf_hvp = _raise_not_implemented_error
                self.cdf_hvp_vec = _raise_not_implemented_error


        

        

    def generate_penalty_parameter(self, autobeta_args = {}):
        '''
            This function generates the penalty parameter (beta) for the constraint dissolving function.
            It uses heuristics based on Monte Carlo sampling to determine an appropriate value.
        '''


        # Set default values or use provided arguments for the penalty parameter calculation.
        if 'max_samples' in autobeta_args.keys():
            max_samples = autobeta_args['max_samples']
        else:
            max_samples = 30

        if 'sample_dist' in autobeta_args.keys():
            sample_dist = autobeta_args['sample_dist']
        else:
            sample_dist = 1e0

        if 'thresholding' in autobeta_args.keys():
            thresholding = autobeta_args['thresholding']
        else:
            thresholding = 1e-5


        if 'epsilon' in autobeta_args.keys():
            epsilon = autobeta_args['epsilon']
        else:
            epsilon = 1e-5

        if 'coeffs' in autobeta_args.keys():
            coeffs = autobeta_args['coeffs']
        else:
            coeffs = 1.2


        if 'first_order' in autobeta_args.keys():
            flag_FO = autobeta_args['first_order']
        else:
            flag_FO = False


        manifold = self.manifold 
        obj_fun = self.obj_fun
        obj_grad = self.obj_grad


        # Local helper functions to flatten and reshape variables according to the manifold.
        local_flatten = lambda var: self.manifold.tensor2array(self.manifold.m2v(var))
        local_reshape = lambda var: self.manifold.v2m(self.manifold.array2tensor(var))


        # Reference point initialization for sampling.
        X_ref = manifold.tensor2array(manifold.m2v(self.Xinit))
        fval_feas_list = []

        for jjj in range(max_samples):
            # Generate a random direction and scale it.
            D = np.random.randn(manifold.var_num)
            D = (D/ np.linalg.norm(D,2)) * np.random.rand()
            
            # Perturb the reference point along the random direction.
            X_ref_tmp = manifold.v2m(manifold.array2tensor(  X_ref + sample_dist * D  ))
            A_X_ref_tmp = manifold.A(X_ref_tmp)

            # Calculate the differences in objective function values based on whether the manifold is a product manifold.
            if manifold.manifold_type == 'P':
                diff_fval = -abs(float(obj_fun( *A_X_ref_tmp )) - float(obj_fun( *manifold.A(A_X_ref_tmp) )))

                if flag_FO:
                    upper =  np.sum((local_flatten(A_X_ref_tmp) - local_flatten(X_ref_tmp))  * local_flatten(self.manifold.JA(A_X_ref_tmp, obj_grad(*A_X_ref_tmp))))
                    lower =  np.abs(np.sum((local_flatten(A_X_ref_tmp) - local_flatten(X_ref_tmp))  * local_flatten(self.manifold.JC(X_ref_tmp, self.C(X_ref_tmp)  )))) + epsilon

            else:
                diff_fval = -abs(float(obj_fun( A_X_ref_tmp )) - float(obj_fun( manifold.A(A_X_ref_tmp) )))

                if flag_FO:
                    upper =  np.sum((local_flatten(A_X_ref_tmp) - local_flatten(X_ref_tmp))  * local_flatten(self.manifold.JA(A_X_ref_tmp, obj_grad(A_X_ref_tmp))))
                    lower =  np.abs(np.sum((local_flatten(A_X_ref_tmp) - local_flatten(X_ref_tmp))  * local_flatten(self.manifold.JC(X_ref_tmp, self.manifold.C(X_ref_tmp)  )))) + epsilon
                # diff_fval = obj_fun( X_ref_tmp ) - obj_fun( A_X_ref_tmp )
            diff_CX =  np.abs(float(manifold.Feas_eval(X_ref_tmp) - manifold.Feas_eval( A_X_ref_tmp ))) ** 2 + epsilon
            

            # Append the candidate values of the penalty parameter in the list. 
            # fval_feas_list.append( (float(diff_fval), float(diff_CX) ) )
            fval_feas_list.append(  2 *max( -float(diff_fval)/float(diff_CX), thresholding )  )

            if flag_FO:
                fval_feas_list.append( max( upper/lower, thresholding  ) )



        # Calculate beta as a coefficient times the maximum value from the candidate values.
        beta = coeffs * max(fval_feas_list)

        return beta



        
            


        
from cmath import sqrt
import numpy as np
import autograd.numpy as anp
from autograd import hessian, grad, jacobian, make_vjp, make_jvp, make_hvp


class backbone_autograd:
    def __init__(self, *args, **kwargs) -> None:
        '''
            Initialize the backbone.
        '''
        
        # Initialize the class with autograd's numpy wrapper functions for linear algebra operations.
        self.solve = anp.linalg.solve 
        self.identity_matrix = anp.eye
        self.zero_matrix = anp.zeros
        self.func_sum = anp.sum 
        self.func_sqrt = anp.sqrt 
        self.var_type = 'numpy'
        
    def dir_grad(self,mappings,X, D):
        # Calculate the directional gradient of a mapping at point X in direction D.
        def local_fun(Y):
            return anp.sum( D * mappings(Y) )
        return grad(local_fun)(X)




    def auto_diff_vjp(self,fun, X, D):
        # Compute the vector-Jacobian product of for function `fun` at point X with vector D.
        fun_vjp, val = make_vjp(fun)(X)
        return fun_vjp(D)

    def auto_diff_jvp(self, fun, X, D):
        # Compute the Jacobian-vector product for function `fun` at point X with vector D.
        val, jvp_result = make_jvp(fun)(X)(D)
        return jvp_result

    def auto_diff_jacobian(self, fun, X):
        # Compute the full Jacobian matrix for function `fun` at point X.
        return jacobian(fun)(X)



    def linear_map_adjoint(fun,D):
        # Define the adjoint of a linear map.
        test_fun = lambda U: anp.sum(D *fun(U))
        return grad(test_fun)
        # return lambda X: auto_diff_vjp(fun, X, D)




    def autodiff(self, obj_fun, obj_grad = None, manifold_type = 'S'):
        if obj_grad is not None:
            local_obj_grad = obj_grad
        else:
            local_obj_grad = grad(obj_fun)



        # def local_obj_hess(X, D):
        #     def directional_grad(X):
        #         return anp.sum( D*  local_obj_grad(X))
        #     return grad(directional_grad)(X)

        local_obj_hess = lambda X, D: self.auto_diff_vjp(local_obj_grad, X, D)
        # local_obj_hess = lambda X, D:  make_hvp(obj_fun, X)(D)

        return local_obj_grad, local_obj_hess


    def array2tensor(self, X_array):
        # Convert an array to the variables of the manifold (identity function in this context).
        return X_array

    def tensor2array(self, X_tensor):
        # Convert the variables of the manifold to an array (identity function in this context).
        return X_tensor


    def jit(self, fun):
        # Just-In-Time compilation (no operation here as autograd does not have JIT).
        # Placeholder for compatibility with other backbones that may support JIT.
        return fun

    

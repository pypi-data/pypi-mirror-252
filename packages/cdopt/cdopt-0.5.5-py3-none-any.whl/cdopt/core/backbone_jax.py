from cmath import sqrt
import numpy as np
import jax
import jax.numpy as jnp

from jax import grad, jvp, vjp,  jit



class backbone_jax:
    def __init__(self, *args, **kwargs) -> None:
    
        # Initialize the class with JAX's linear algebra functions.
        self.solve = jnp.linalg.solve 
        self.identity_matrix = jnp.eye
        self.zero_matrix = jnp.zeros
        self.func_sum = jnp.sum 
        self.func_sqrt = jnp.sqrt 
        self.var_type = 'jax'
    

        # Set the device for JAX computations, defaulting to the first CPU device.
        if 'device' in kwargs.keys():
            self.device = kwargs['device']
        else:
            self.device = jax.devices('cpu')[0]
        
    def dir_grad(self,mappings,X, D):
        # Calculate the directional gradient of a function 'mappings' at point X in direction D.
        def local_fun(Y):
            return jax.sum( D * mappings(Y) )
        return grad(local_fun)(X)




    def auto_diff_vjp(self,fun, X, D):
        # Compute the vector-Jacobian product for function `fun` at point X with vector D.
        val, fun_vjp = vjp(fun, X)
        return fun_vjp(D)[0]

    def auto_diff_jvp(self, fun, X, D):
        # Compute the Jacobian-vector product for function `fun` at point X with vector D.
        val, jvp_result = jvp(fun, (X,), (D,))
        return jvp_result

    def auto_diff_jacobian(self, fun, X):
        # Compute the full Jacobian matrix for function `fun` at point X using reverse-mode autodiff.
        return jax.jacrev(fun)(X)



    def linear_map_adjoint(fun,D):
        # Define the adjoint of a linear map represented by function `fun` with respect to vector D.
        test_fun = lambda U: jnp.sum(D *fun(U))
        return grad(test_fun)
        # return lambda X: auto_diff_vjp(fun, X, D)




    def autodiff(self, obj_fun, obj_grad = None, manifold_type = 'S'):
        # Automatically differentiate the objective function `obj_fun`.
        # If the gradient `obj_grad` is provided, use it; otherwise compute it using JIT compilation for efficiency.
        if obj_grad is not None:
            local_obj_grad = obj_grad
        else:
            local_obj_grad_tmp = jit(grad(obj_fun))
            local_obj_grad = lambda X: local_obj_grad_tmp(X)


        # def local_obj_hess(X, D):
        #     def directional_grad(X):
        #         return anp.sum( D*  local_obj_grad(X))
        #     return grad(directional_grad)(X)

        local_obj_hess = lambda X, D: self.auto_diff_vjp(local_obj_grad, X, D)
        # local_obj_hess = lambda X, D:  make_hvp(obj_fun, X)(D)

        return local_obj_grad, local_obj_hess


    def array2tensor(self, X_array):
        # Convert a NumPy array to the variables of the manifold. 
        return jax.device_put(jnp.asarray(X_array), device=self.device)

    def tensor2array(self, X_tensor):
        # Convert the variables of the manifold. back to a NumPy array.
        return np.array(X_tensor,dtype=np.float64 ,order = 'F')


    def jit(self, fun):
        # Compile the function `fun` using JAX's JIT compiler for improved performance.
        return jax.jit(fun)

    

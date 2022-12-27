import streamlit as st

from random import randint
from functools import wraps
import inspect, itertools

from app import init_state
from streamlit import session_state as state

AUTOWIDGETS_KEY = "_AUTOWIDGETS"



init_state(AUTOWIDGETS_KEY, {})
wstate = state[AUTOWIDGETS_KEY]

def _get_arg_from_state(func_name, argument, default=None):
    if func_name in wstate and argument in wstate[func_name]:
        return wstate[func_name][argument]
    return default


def _get_args_dict(func, args, kwargs, include, exclude):
    boundargs = inspect.signature(func).bind(*args, **kwargs)
    boundargs.apply_defaults()
    return boundargs.arguments


def _create_widgets(func, args_dict):

    key_template = "{funcname}_{{argname}}_{rnd_id:0>20}".format_map(dict(funcname=func.__name__, rnd_id=randint(1,10e8)))

    func_name = func.__name__

    if st.button("delete funcstate"):
        del wstate[func_name]

    
    if func_name not in wstate:
        wstate[func_name] = {}
    
    func_state = wstate[func_name]
    

    print("XXXXXX")
    print(f"{func_state=}")
    d = {}
    for k,v in args_dict.items():
        # if include and k not in include:
        #     continue
        # if exclude and k in exclude:
        #     continue
        key=key_template.format(argname=k)
        d[k] = st.text_input(k, value=func_state.get(k, v), key=key)
    
    return d


# TODO: aceitar kwargs da func na factory com o 'tipo' de widget para criar
# por exemplo, passar uma lista de opçoes para criar um


class Param:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def stfy_factory(*_args, container=None, include=None, exclude=[], widgets_position="above", **_kwargs):

    if widgets_position.lower() not in ["above", "below"]:
        raise ValueError("widgets_position not in ['above', 'below']")

    def stfy(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            args_dict = _get_args_dict(func, args, kwargs, include, exclude)

            nonlocal container
            if container is None:
                container = st.container()
            
            with container:
                st.write("##### Input")
                inputs = {}
                for k,v in args_dict.items():
                    inputs[k] = st.text_input(k, value=_get_arg_from_state(func_name, k) or v)
            
                print(f"{inputs=}")

                st.write("##### Output")
                res = func(**inputs)
                if func_name not in wstate:
                    wstate[func_name] = {}
            #func_state = wstate[func_name]
            
            
            return res
        
        return wrapper
    
    return stfy


if __name__=="__main__":

    print("\n\nSTART RUN\n")

    st.header("stfy")
    st.write("Automagicamente cria widgets para os argumentos de uma função")

    st.subheader("Example 1")
    with st.echo(code_location="above"):
        @stfy_factory()
        def foo(arg1):
            st.write(f"this is foo({arg1})")
            print(f"this is foo({arg1})")
        
        foo(arg1=1)

        foo(arg1=2)
    
    # st.subheader("Example 2")
    # with st.echo(code_location="above"):
    #     @stfy_factory(include=['kwarg1'], exclude=['kwarg2'])
    #     def foo2(arg1, arg2, kwarg1=1, kwarg2=2):
    #         print(f"this is foo2({arg1}, {arg2}, {kwarg1=}, {kwarg2=})")
        
    #     foo2(arg1=1, arg2="text", kwarg1=['option1', 'option2'])
    

    # st.subheader("Example 3")
    # with st.echo(code_location="above"):
    #     @stfy_factory(widgets_position="above")
    #     def foo(a=1):
    #         msg = f"This is foo, {a=}"
    #         st.markdown(f"```{msg}```")
    #         print(msg)
        
    #     foo(3)
    


    print("\n\END RUN\n")
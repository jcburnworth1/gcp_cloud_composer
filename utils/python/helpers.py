## Import Libraries
import os

class Helpers:

    @staticmethod
    def print_default_args(default_args):
        """
        Print default arguments
        :return: None
        """
        print(f'########## default_args: {default_args} ##########')

    @staticmethod
    def print_params(params):
        """
        Print default params
        :return: None
        """
        print(f'########## Params: {params} ##########')

    @staticmethod
    def print_env():
        """
        Print environment variables
        :return: None
        """
        print(f"##### Env Vars: {os.environ} #####")

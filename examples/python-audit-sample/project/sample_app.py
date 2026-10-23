"""Audit fixture only; do not run this module."""
import subprocess


def evaluate_user_expression(expression):
    return eval(expression)


def run_user_command(command):
    return subprocess.run(command, shell=True, check=False)

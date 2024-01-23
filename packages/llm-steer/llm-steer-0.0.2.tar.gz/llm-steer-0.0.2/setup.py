from setuptools import setup

setup(
    name='llm-steer',
    version='0.0.2',
    description='Steer LLM responses towards a certain topic/subject and enhance response capabilities using activation engineering by adding steer vectors',
    author='Mihai Chirculescu',
    author_email='apropodemine@gmail.com',
    py_modules=['steer_llm'],
    url="https://github.com/Mihaiii/SteerLLM",
    install_requires=[
        'transformers'
    ],
)
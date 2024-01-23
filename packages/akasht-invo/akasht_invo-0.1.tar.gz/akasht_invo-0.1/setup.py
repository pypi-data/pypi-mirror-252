from setuptools import setup, find_packages

setup(
    name='akasht_invo',
    version='0.1',
    packages=find_packages(),
    description='Mst maal hai',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HuiHui',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your_package',
    install_requires=[
        'agents','autonomous_agents','utilities','tot','tools','tabular_synthetic_data',
        'synthetic_data','sql','smart_llm','rl_chain','retrievers','pydantic_v1','prompts','prompt_injection_identifier','plan_and_execute','pal_chain',
        'openai_assistant','open_clip','llms','llm_symbolic_math','llm_bash','graph_transformers','generative_agents','fallacy_removal','data_anonymizer',
        'cpal','comprehend_moderation','chat_models'
    ],
)

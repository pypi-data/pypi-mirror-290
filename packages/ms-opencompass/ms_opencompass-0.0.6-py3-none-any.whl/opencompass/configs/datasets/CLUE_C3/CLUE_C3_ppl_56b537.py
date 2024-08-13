from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import PPLInferencer
from opencompass.openicl.icl_evaluator import AccEvaluator
from opencompass.datasets import C3Dataset

C3_reader_cfg = dict(
    input_columns=[
        'question', 'content', 'choice0', 'choice1', 'choice2', 'choice3',
        'choices'
    ],
    output_column='label')

C3_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template={
            0: '文章：{content}\n问题：{question}\n答案：{choice0}',
            1: '文章：{content}\n问题：{question}\n答案：{choice1}',
            2: '文章：{content}\n问题：{question}\n答案：{choice2}',
            3: '文章：{content}\n问题：{question}\n答案：{choice3}'
        }),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=PPLInferencer))

C3_eval_cfg = dict(evaluator=dict(type=AccEvaluator))

C3_datasets = [
    dict(
        type=C3Dataset,
        abbr='C3',
        path='./data/CLUE/C3/dev_0.json',
        reader_cfg=C3_reader_cfg,
        infer_cfg=C3_infer_cfg,
        eval_cfg=C3_eval_cfg)
]

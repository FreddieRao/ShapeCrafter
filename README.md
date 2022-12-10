## ShapeCrafter: A Recursive Text-Conditioned 3D Shape Generation Model (NeurIPS 2022)<br><sub>PyTorch implementation </sub>

![Teaser image](./doc/teaser.gif)

**ShapeCrafter: A Recursive Text-Conditioned 3D Shape Generation Model**<br>
[Rao Fu](https://freddierao.github.io/), 
[Xiao(Sean) Zhan](https://seanzhan.com/#/), 
[Yiwen Chen](https://cs.brown.edu/people/grad/ychen485/),
[Daniel Ritchie](https://dritchie.github.io/),
[Srinath Sridhar](https://cs.brown.edu/people/ssrinath/) <br>
**[Paper](https://arxiv.org/abs/2207.09446)
, [Project Page](https://ivl.cs.brown.edu/#/projects/shapecrafter)**

Abstract: *We present ShapeCrafter, a neural network for recursive text-conditioned 3D shape generation. Existing methods to generate text-conditioned 3D shapes consume an entire text prompt to generate a 3D shape in a single step. However, humans tend to describe shapes recursively-we may start with an initial description and progressively add details based on intermediate results. To capture this recursive process, we introduce a method to generate a 3D shape distribution, conditioned on an initial phrase, that gradually evolves as more phrases are added. Since existing datasets are insufficient for training this approach, we present Text2Shape++, a large dataset of 369K shape-text pairs that supports recursive shape generation. To capture local details that are often used to refine shape descriptions, we build on top of vector-quantized deep implicit functions that generate a distribution of high-quality shapes. Results show that our method can generate shapes consistent with text descriptions, and shapes evolve gradually as more phrases are added. Our method supports shape editing, extrapolation, and can enable new applications in human-machine collaboration for creative design.*

## Preparing datasets

ShapeCrafter is trained with [Text2Shape++](https://1drv.ms/u/s!Ai-PFrdirDvwkTqchX1OXpEQnCnk?e=xtkgSu) dataset, which is built upon [Text2Shape](http://text2shape.stanford.edu/) dataset. We provide the script for converting Text2Shape dataset to Text2Shape++ dataset. It enables converting any one(sentence)-to-one(shape) dataset, i.e., [ShapeGlot](https://ai.stanford.edu/~optas/shapeglot/) dataset, to many(phrases)-to-many(shapes) dataset. Please refer the [readme](./ConstituencyParsing/README.md)


## TODOs
* Code will be released soon.
* Pretrained weights will be released soon.

## Citation

```latex
@inproceedings{
fu2022shapecrafter,
title={ShapeCrafter: A Recursive Text-Conditioned 3D Shape Generation Model},
author={Rao Fu and Xiao Zhan and Yiwen Chen and Daniel Ritchie and Srinath Sridhar},
booktitle={Advances in Neural Information Processing Systems},
editor={Alice H. Oh and Alekh Agarwal and Danielle Belgrave and Kyunghyun Cho},
year={2022},
url={https://openreview.net/forum?id=KUOKpojFr_}
}
```
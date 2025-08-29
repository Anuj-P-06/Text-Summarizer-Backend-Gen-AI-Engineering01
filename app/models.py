from pydantic import BaseModel, Field
from typing import Annotated


class SummarizeRequest(BaseModel):
    text: Annotated[
        str,
        Field(
            title="Enter Text",
            description="Text to be summarized",
            example="Dinosaurs are varied from taxonomic, morphological and ecological standpoints. Birds, at over 11,000 living species, are among the most diverse groups of vertebrates. Using fossil evidence, paleontologists have identified over 900 distinct genera and more than 1,000 different species of non-avian dinosaurs. Dinosaurs are represented on every continent by both extant species (birds) and fossil remains. Through most of the 20th century, before birds were recognized as dinosaurs, most of the scientific community believed dinosaurs to have been sluggish and cold-blooded. Most research conducted since the 1970s, however, has indicated that dinosaurs were active animals with elevated metabolisms and numerous adaptations for social interaction. Some were herbivorous, others carnivorous. Evidence suggests that all dinosaurs were egg-laying, and that nest-building was a trait shared by many dinosaurs, both avian and non-avian."
        )
    ]

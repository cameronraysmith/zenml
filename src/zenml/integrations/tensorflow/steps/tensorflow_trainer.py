#  Copyright (c) ZenML GmbH 2021. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import pandas as pd
import tensorflow as tf

from zenml.steps.step_interfaces.base_trainer_step import (
    BaseTrainerConfig,
    BaseTrainerStep,
)


class TensorflowBinaryClassifierConfig(BaseTrainerConfig):
    layers = [32, 64, 1]
    input_shape = [8]
    learning_rate = 0.001
    metrics = ["accuracy"]
    epochs = 50
    target_column: str = None
    batch_size = 32


class TensorflowBinaryClassifier(BaseTrainerStep):
    def entrypoint(
        self,
        train_dataset: pd.DataFrame,
        validation_dataset: pd.DataFrame,
        config: TensorflowBinaryClassifierConfig,
    ) -> tf.keras.Model:
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Flatten(input_shape=config.input_shape))

        for layer in config.layers:
            model.add(tf.keras.layers.Dense(layer))

        model.compile(
            optimizer=tf.keras.optimizers.Adam(config.learning_rate),
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=config.metrics,
        )

        train_target = train_dataset.pop(config.target_column)
        validation_target = validation_dataset.pop(config.target_column)
        model.fit(
            x=train_dataset,
            y=train_target,
            validation_data=(validation_dataset, validation_target),
            batch_size=config.batch_size,
            epochs=config.epochs,
        )

        return model

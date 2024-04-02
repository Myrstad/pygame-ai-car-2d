# AI CAR (2D)

This is a project centered around creating the best AI to drive around a track
the track can be made using the `make_course.py` more about that in [getting started](#getting-started) and [usage](#usage)

## Getting started

You can clone this reposity via the download (Zip) option or run the folliwing commands to get started:

```
$ git clone https://github.com/Myrstad/IT2-norway-weather.git my-dir
$ cd ./my-dir
$ python3 -u main.py
```

## Usage

### Saving, loading and training models

This is all done in `settings.py`
* ENVIORONMENT_PATH: is the relative path to the circuit
* TRAINED_MODEL_PATH: is the relative path to a saved model (leave as None if you want to train from scratch)
* CURRENT_MODEL_NAME: used for saving the model to `models/{name}.pkl`

Tweaking the learning rate and population size (the machine learning paramaters) are also set in `settings` under:
* LEARNING_RATE: if set to 0 it will not learn
* POPULATION_SIZE: has to be greater than or equals 4, or 1 when learning rate is 0

### Creating a new circuit/ course

Follow this to make your own circuit:

* Change where the circuit will get saved and be named
* Press 1 and make the outer walls
* Press 2 and make the inner walls
* Press `p` to set the start position
* Press `d` to set the start direction (a vector from start point to where you press)
* Press `m` for reward gates.
  - The sequencing matters
  - Therefore make the reward gates around the circuit
  - The first reward gate is where the car should ideally go after training
  - There may be a need for many gates if the circuit is hard

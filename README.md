# whosthatbird-quiz

# Introduction
Welcome to Whosthatbird-quiz! This project is a simple quiz game that tests your knowledge of bird species by playing you the song or call of a bird and asking you to guess the species name. It was developed as a final project for Harvard's CS50 class 2023 and is a fun way to learn about different bird species and challenge yourself.

# How to Play
You will hear a recording of a bird's song or call, and below it, you will see buttons, where you can guess for the species name.

If you're not sure about the answer, you can click on the "Hint" button, which will give you a clue about the bird's species. The hint button will display a map using Leaflet with the coordinates of the location where the recording was made. This can be helpful in narrowing down your guess for the bird's species.

You can also skip a question by clicking on the "Skip" button.

Once you have entered your guess, click on the "Submit" button. If your answer is correct, you will see a green checkmark, and if it's incorrect, you will see a red X.

At the end of the quiz, you will see your score and the option to play again.

# Development
This project was developed as a final project for Harvard's CS50 class 2023. It was built using Flask, a Python web framework, and deployed on Heroku. The bird recordings and species data were sourced from the Xeno-Canto.org library.

The hint feature was added using Leaflet, an open-source JavaScript library for interactive maps. The coordinates of the sound file were obtained from the Xeno-Canto API and used to create the map.

If you would like to contribute to the project, feel free to fork the repository and submit a pull request. We welcome contributions and feedback from the community.

# Acknowledgements
We would like to thank Xeno-Canto.org for providing the bird recordings and species data used in this project. We would also like to express our gratitude to Harvard's CS50 class 2023 for providing us with the opportunity to work on this project.

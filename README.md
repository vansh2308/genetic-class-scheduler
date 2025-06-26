# Genetic Scheduler (NSGA-II)

This project is a class scheduler based on genetic algorithms, specifically the NSGA-II (Non-dominated Sorting Genetic Algorithm II). It aims to solve the complex problem of creating optimal university class schedules by considering various constraints and objectives.

## Features

- **Multi-objective Optimization**: Uses NSGA-II to handle multiple, often conflicting, objectives such as minimizing professor conflicts, respecting room capacities, and accommodating student group preferences.
- **JSON Configuration**: Class schedules, professor details, room information, and other constraints are defined in a flexible `Input.json` file.
- **HTML Output**: Generates a clear and easy-to-read HTML representation of the final, optimized schedule.
- **Extensible**: The modular design allows for the addition of new constraints and objectives.

## How to Run

1.  **Prerequisites**: Make sure you have Python 3 and `pip` installed.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Scheduler**:
    ```bash
    python main.py
    ```
    This will use the default `Input.json` file.

4.  **Custom Input**: You can also provide a path to your own JSON input file as a command-line argument:
    ```bash
    python main.py /path/to/your/input.json
    ```

5.  **View the Output**: The script will automatically open the generated HTML schedule in your default web browser.

## Input File Format

The `Input.json` file contains an array of objects, each representing a professor, course, room, student group, or class. Here's a brief overview:

-   **`prof`**: Defines a professor with an `id` and `name`.
-   **`course`**: Defines a course with an `id` and `name`.
-   **`room`**: Defines a room with a `name`, `lab` (boolean), and `size`.
-   **`group`**: Defines a student group with an `id`, `name`, and `size`.
-   **`class`**: Defines a class to be scheduled, linking a `professor`, `course`, and `groups`. It also specifies the `duration` and whether it's a `lab` session.


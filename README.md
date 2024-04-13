<h1> Mythic-Quest </h1>

Welcome to my GitHub repository for a dynamic browser game reminiscent of Gladiatus and Bite Fight! Built using Django, Python, HTML, CSS, and JavaScript, this project offers players the thrill of creating characters, engaging in battles with others, venturing into dungeons to face monsters, and even seeking refuge in the tavern to heal. With features like potion shops to enhance stats and a robust support system facilitated by web3forms API, players can immerse themselves in a rich gaming experience. Utilizing Django Template Language and a blend of class-based and function-based views, the game boasts seamless authentication, ensuring secure user accounts. With over 20 pages, a mix of custom CSS and Bootstrap styling, and both public and private sections, users can easily navigate their gaming journey. Admins wield full control, while Game Masters oversee character interactions, making for an engaging and immersive gameplay environment.

<h3> Setup Instructions: </h3>

1. Clone the repository to your local machine:
    - git clone https://github.com/scarecrow405/Mythic-Quest.git

2. Navigate to the project directory:
    - cd project-directory

3. Install dependencies:
    - pip install -r requirements.txt

4. Create media directory:
    - in your project at manage.py level, create a directory called "media".

5. Apply migrations:
    - python manage.py migrate

6. Seed the database with initial data:
    - python manage.py seed_monsters
    - python manage.py seed_items

7. Run the development server:
    - python manage.py runserver

8. Access the application at:
    - http://localhost:8000

<h3> Additional Notes:</h3>
Be sure to set up your database and make other adjustments on your set up to run this project.

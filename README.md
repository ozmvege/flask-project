# Flask Webapp
#### Description:


ai.html
Now ai.html is chatbot that is powered by openai's api.
Also the api key is expired.
So it cant be used till a valid api key gets entered in /static/key.txt and /static/chat.js
There isnt much more to it, i tried to make it fancy with css and bootstrap features
The messages dont get saved in the db.

ml.html
Here i wanted to implement a notify page and it has all functionality.
It recognizes when no mail is entered oder the mail is already in the db for ml_notify
In the background a video is playing and yeah its just a classic notify page.

Chatbot (ai.html):
The chatbot implemented in the webapp is powered by OpenAI's API. It serves as an interactive interface where users can have conversations with the chatbot. However, currently, the chatbot functionality is disabled due to an expired API key. To enable the chatbot, a valid API key needs to be entered into the "/static/key.txt" and "/static/chat.js" files. The chatbot's frontend is designed with CSS and features from Bootstrap, giving it a visually appealing and user-friendly interface. It's worth noting that the chatbot messages are not stored in the database, and the conversations are not persisted beyond the session.

ML Notify Tool (ml.html):
The ML (Machine Learning) Notify tool is fully functional and provides a convenient way to send notifications to users via email. When using the ML Notify tool, users are required to enter an email address to receive the notifications. The system intelligently checks whether an email is missing or if the provided email address is already present in the database for the "ml_notify" table. This helps avoid redundant notifications to the same user.

The ML Notify tool utilizes a video playing in the background to enhance the user experience while using the page. The video creates an engaging and dynamic backdrop for the notification feature, making the webapp more appealing to users.

Database Structure:
The webapp relies on a relational database to store user information and other relevant data. The database schema consists of two main tables: "users" and "user_details." The "users" table holds essential user account information, such as the username and password. The "user_details" table contains additional user data, such as first name, last name, etc., and is connected to the "users" table via a foreign key relationship. This approach ensures a well-organized and efficient data management system for user information.

Password Security:
During the registration process, the webapp takes password security seriously by enforcing certain criteria for password creation. The password must meet predefined criteria, which can be adjusted as needed to adapt to changing security requirements. The criteria may include parameters such as minimum length, special characters, uppercase letters, and numbers. By setting these criteria, the webapp enhances the security of user accounts and protects against weak passwords.

Forgot Password Functionality:
While the webapp features a sophisticated login and registration system, it also plans to include a "Forgot Password" functionality. Unfortunately, this functionality is not yet implemented, but it remains a future enhancement to improve user experience and account recovery.

Navigation and User Interface:
The webapp boasts a modern and intuitive design with a dark mode switch, providing users with a personalized and visually appealing experience. The navigation bar includes essential elements such as links to GitHub and Twitter profiles, a logout button, a home button, and navigation buttons for easy access to different sections of the webapp.

Conclusion:
The Flask webapp is a well-rounded project that showcases various functionalities, including a sophisticated login and registration system, an interactive chatbot powered by OpenAI's API (pending API key update), and a fully functional ML Notify tool for email notifications. The elegant design and user-friendly interface contribute to a positive user experience while interacting with the webapp's different features. With future improvements, such as implementing the "Forgot Password" functionality, the webapp is poised to become even more robust and user-centric.

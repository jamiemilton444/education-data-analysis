Our code addresses educational inequality. We focused on the disparities across different schools, specifically a focus on Black students. To explore this issue,  we zeroed in on the differences in the percentage of Black students at each school, funding per student, and test scores.

We narrowed our scope to high schools in Bristol County, Massachusetts. The website we developed presents data on each school, allowing users to explore the relationship between racial demographics, school funding, and student performance on the 9th and 10th-grade MCAS tests in math, science, and English. Users are able to input their desired school, and our website will give them back the information or their school in comparison to the other high schools in Bristol County; it does this visually with bar graphs, as well.

1. Make sure you are inside of the fp dreams folder and are using python3.
2. Make sure you have the flask app installed. If not, type in: pip install flask
3. Make sure you have pandas downloaded. If not, type in the terminal: pip install pandas
4. To run this code, open the file named fp.py and hit the run button in the top right corner. A (1) will appear near "PORTS", and a pop up will come up in the bottom left corner.
5. To be redirected to the website, you can hit the pop up, or go to "PORTS" and click the globe symbol near the link under "Forwarded Address".
6. Type a school from Bristol County into the bar.

In terms of generative AI tools, we used it for a better understanding of how to create our bar graphs, specifically the code for create_bar_graph(). Because this was a new concept to us, it was difficult, especially figuring out how to show the bars side by side for the schools. AI tools helped us know how to use uuid.uuid4() to generate specific  filenames for each chart.


Another way we used generative AI tools was in terms of actually customizing the webpage with CSS in Flask. This is the part of our code using render_template_string(). While we could handle basic HTML, designing an aesthetically pleasing layout (with background images, transparency, and custom fonts) was new to us. We used ChatGPT to suggest CSS styles and layout ideas, and then customized them to match the theme of our project.

The final way in which we used it was for the fuzzy matching. This was the part of our code using diff lib.get_close_matches and find_best_match(). We knew we needed a way to handle typos or variations in school names. So, we took what we learned from class and what the AI tool could help us to be more informed about in terms of string matching to make this part effective. 

Also, we grabbed our CSV file’s data from Massachusetts’ Department of Education! https://www.doe.mass.edu

# Relational-Algebra-Query-Processor

Relational Algebra Processor

![image](https://github.com/JJPelk/Relational-Algebra-Query-Processor/assets/146587699/d3d24da6-eaf2-49a5-a2bb-a684d4c33dd5)

This application provides a graphical user interface for performing relational algebra operations on user-defined relations. A dynamic table allows users to input tuple data hassle free and without syntax, resizing to any table size neccesarry. 

Features:
- Add and remove rows and columns to define relations.
- Enter the relation name, attributes, and tuples via a dynamic table.
- Perform relational algebra operations such as select, project, join, union, set difference, and intersection.
- Display results of the relational algebra queries.

Supported Operations:
- select: Filters tuples from a relation based on a condition (e.g., "select Age>30(Employees)").
- project: Reduces a relation to certain attributes (e.g., "project(Employees, EID, Name)").
- join: Combines two relations based on a common attribute (e.g., "join(Employees, Departments)") or "join(Employees, Departments, EID == ManagerEID)" 
  for joins without common columns).
- union: Combines two relations with the same schema (e.g., "union(Relation1, Relation2)").
- set_difference: Finds tuples in one relation but not in another (e.g., "set_difference(Relation1, Relation2)").
- intersection: Finds tuples common to two relations (e.g., "intersection(Relation1, Relation2)").

Syntax:
- Relations are entered in a tabular format with the first text box specifying the relation name.
- Queries are entered in a text box below the relation input area using the format "operation(arguments)".

Installation:
To run the Relational Algebra Processor, ensure that Python is installed on your system. Then, install the required packages using the command:

pip install -r requirements.txt

The requirements.txt file includes all the necessary packages. Ensure you are in the same directory as the requirements.txt file when running the pip install command.

Usage:
Run the program by executing the main.py script:

python main.py

Once the application window is open, you can begin by entering relations and performing queries as described above.





ASSIGNMENT INSTRUCTIONS:

"Instructions
Students are tasked with designing a system similar to "Relax" that is capable of accepting text representing relations and relational algebra queries.

Example of a Relation:

Employees (EID, Name, Age) = {
E1, John, 32
E2, Alice, 28
E3, Bob, 29
}
Example of a Relational Algebra Query:

select Age>30(Employees)
Project Requirements:

Parse the given text and relational algebra query.
Convert the relations into a suitable data structure.
Convert the relational algebra query into an ordered list of operations.
Display the result of the query based on the provided relations.
Grading Criteria:

The system must be general. It is unacceptable to submit a system that only works with hard-coded examples.
Your system should support at least the following operations: selection, projection, join, and set operators. If not, please do not submit it.
Create a video illustrating the functionality of your system.
Upload your code to GitHub and share the link in Brightspace.
Points and Benefits: The project carries a weightage of 5 extra points. While there's no penalty for not submitting, students who complete this project can utilize these extra points to cover potential losses in other assessments such as assignments and the final project.

Deadline: You have 2 weeks to complete this project.

Note: You're welcome to seek assistance from ChatGPT, but ensure you comprehend every piece of code you write, as there will be a discussion about it. Only a few students might be able to complete this challenge, and I will personally grade those submissions."

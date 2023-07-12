import tkinter as tk
import re
import numpy as np

from scipy.optimize import linprog

def get_input():
	objective_function = objective_textbox.get("1.0", "end-1c")  # Get objective function
	constraints = constraints_textbox.get("1.0", "end-1c")  # Get constraints
	is_MAX = re.search("MAX",objective_function)
	print("Objective_function:\n"+ objective_function + "\nconstraints:\n" + constraints)

	obj_func = "MAX Z = 3x1 + 5x2"

	# Extracting coefficients from the objective function
	obj_func = obj_func.split(" = ")[1]
	coeffs = obj_func.split(" + ")
	variable_num = len(coeffs)
	for i in range(len(coeffs)):
		coeffs[i]= coeffs[i].split("x")[0]
		if is_MAX != None:
			coeffs[i]= -int(coeffs[i])
		else:
			coeffs[i]= int(coeffs[i])
	
	
	A=[]
	b=[]
	constraints_list= constraints.split("\n")
	print("constslists:"+ str(constraints_list))

	for i in range(len(constraints_list)-1):
		print("constraints list i="+ str(i))
		print("A:" + str(A))
		print("b:" + str(b))
		#if re.search(">=",constraints_list)!="None" and re.search(">=",constraints_list)!="None":
		if re.search(">=",constraints_list[i])!="None":
			symbol=">="
		if re.search("<=",constraints_list[i])!="None":
			symbol="<="
		b.append(int(constraints_list[i].split(symbol)[1]))
		value_list=[]
		divided= constraints_list[i].split(symbol)[0].split("+")
		for k in range(len(divided)):
			
			constraint_exes = divided[k].split("x")
			value_list.append(constraint_exes[0])
		
		A.append(value_list)

	#print("A =", A)
	#print("b =", b)

	# A = [[1, 0], [0, 1], [3, 2]]
	# b = [4, 6, 18]

	result = linprog(coeffs, A_ub=A, b_ub=b, method='revised simplex')
	opt_solution = result.x
	solution = "Objective Function: {}\nConstraints: {}\n\nSolution:\n".format(objective_function, constraints) + str(opt_solution)
	
	# Clear the previous solution text
	solution_textbox.delete("1.0", "end")
	
	# Display the solution
	solution_textbox.insert("end", solution)
	

		
root = tk.Tk()
root.title('Revised Simplex Calculator')

# Header
header_label = tk.Label(root, text="Type your linear programming problem")
header_label.pack()

# Objective Function Title
objective_label = tk.Label(root, text="Objective Function")
objective_label.pack()

# Objective Function Input Box
objective_textbox = tk.Text(root, height=2, width=60)
objective_textbox.insert("end", "MAX Z = 3x1 + 5x2")
objective_textbox.pack()

# Constraints Title
constraints_label = tk.Label(root, text="Constraints")
constraints_label.pack()

# Constraints Input Box
constraints_textbox = tk.Text(root, height=6, width=60)
constraints_textbox.insert("end", "1x1 + 0x2 <= 4\n0x1 + 1x2 <= 6\n3x1 + 2x2 <= 18\n1x1 + 0x2 >= 0")
constraints_textbox.pack()

# Create button to retrieve input
button = tk.Button(root, text="Solve", command=get_input)
button.pack()

# Frame to display the solution
solution_frame = tk.Frame(root)
solution_frame.pack()

# Solution Textbox
solution_textbox = tk.Text(solution_frame, height=12, width=60)
solution_textbox.pack()

root.mainloop()
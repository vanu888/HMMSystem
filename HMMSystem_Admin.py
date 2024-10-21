import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import os

# Sample data structure to hold patients records
patients = {}
current_password = "password"  # current password
password_file = "current_password.json"  # File to store the current password
data_file = "patients.json"  # File to store patients data using json

#Create main application
class HospitalMedicineManagementAdminApp:
    def __init__(self, root):
        self.root = root # Main window name as root
        self.root.title("Hospital Medicine Management System - Admin") # Main title
        self.root.geometry("800x600") # Window frame size
      
        # Load password file
        self.load_password()
        # Load saved patients data
        self.load_patients()

        # Create style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        self.style.configure("TEntry", background="#ffffff", font=("Arial", 12))
        self.style.configure("TButton", background="#4CAF50", foreground="white", font=("Arial", 12, "bold"))
        self.style.map("TButton", background=[("active", "#45a049")])
        self.style.configure("TNotebook", padding=[5, 5])
        self.style.configure("TNotebook.Tab", padding=[15, 8], font=("Arial", 12, "bold"))

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        self.login_tab = ttk.Frame(self.notebook)
        self.update_tab = ttk.Frame(self.notebook)
        self.display_tab = ttk.Frame(self.notebook)
        self.updateStatus_tab = ttk.Frame(self.notebook)
        self.check_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.login_tab, text="Login")
        self.notebook.add(self.display_tab, text="Patients Data")
        self.notebook.add(self.updateStatus_tab, text="Update Status")
        self.notebook.add(self.update_tab, text="Update Data")
        self.notebook.add(self.check_tab, text="Check") 
        self.notebook.add(self.about_tab, text="About")


        self.create_login_tab()
        self.create_update_tab()
        self.create_display_tab()
        self.create_updateStatus_tab()
        self.create_check_tab()
        self.create_about_tab()

        # Disable all tabs except login
        self.lock_tabs()

        # Show welcome screen
        self.show_welcome_screen()

    #Function to show welcome screen
    def show_welcome_screen(self):
        self.welcome_window = tk.Toplevel(self.root)
        self.welcome_window.title("Hospital Medicine Management System - Admin") # Title to welcome screen 
        self.welcome_window.geometry("800x600") # Size for welcome screen frame
        self.welcome_window.configure(bg="#f0f0f0") # Set background color
        
        # Welcome screen detalis
        loading_label = ttk.Label(self.welcome_window, text="Loading, please wait...", background="#f0f0f0", font=("Arial", 14))
        loading_label.pack(pady=20)

        # Display a loading bar
        self.loading_bar = ttk.Progressbar(self.welcome_window, orient="horizontal", length=300, mode="indeterminate")
        self.loading_bar.pack(pady=10)
        self.loading_bar.start()

        self.welcome_window.after(5000, self.close_welcome_screen)
    
    # Function to close the welcome screen
    def close_welcome_screen(self):
        self.loading_bar.stop()
        self.welcome_window.destroy()
        self.root.deiconify()
        self.notebook.select(self.login_tab)
        
    # Create login tab
    def create_login_tab(self):
        self.login_frame = ttk.Frame(self.login_tab)
        self.login_frame.pack(fill="both", expand=True)

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.change_password_button = ttk.Button(self.login_frame, text="Change Password", command=self.change_password)
        self.change_password_button.pack(pady=10)

    #Fuction to lock the tabs
    def lock_tabs(self):
        for i in range(1, 6):  # Disable all tabs except the first (login)
            self.notebook.tab(i, state='disabled')

    def unlock_tabs(self):
        for i in range(1, 6):  # Enable all tabs except the first (login)
            self.notebook.tab(i, state='normal')

    # Function for login       
    def login(self):
        password = self.password_entry.get()
        if password == current_password:  # Only check the password
            messagebox.showinfo("Login", "Login successful!")
            self.unlock_tabs()  # Unlock tabs on successful login
            self.notebook.select(self.display_tab)  # Switch to the display tab
        else:
            messagebox.showerror("Login", "Invalid password!")
            self.lock_tabs()  # Keep tabs locked if login fails
    
    
    # Create a window to change password 
    def change_password(self):
        # Create a new window for changing the password
        self.change_password_window = tk.Toplevel(self.root)
        self.change_password_window.title("Change Password")
        self.change_password_window.geometry("300x200")
        
        # Old Password Entry
        old_password_label = ttk.Label(self.change_password_window, text="Old Password:")
        old_password_label.pack(pady=5)
        self.old_password_entry = ttk.Entry(self.change_password_window, show="*")
        self.old_password_entry.pack(pady=5)

        # New Password Entry
        new_password_label = ttk.Label(self.change_password_window, text="New Password:")
        new_password_label.pack(pady=5)
        self.new_password_entry = ttk.Entry(self.change_password_window, show="*")
        self.new_password_entry.pack(pady=5)

        # Submit Button
        submit_button = ttk.Button(self.change_password_window, text="Submit", command=self.submit_new_password)
        submit_button.pack(pady=10)
    
    # Load the current password from the file
    def load_password(self):
        global current_password
        if os.path.exists(password_file):
            with open(password_file, 'r') as f:
                data = json.load(f)
                current_password = data.get("password", "password")  # Default password if not  ( use as password )
                
    # Save the new password to the file
    def save_password(self):
        with open(password_file, 'w') as f:
            json.dump({"password": current_password}, f)

    # Function for submit new password
    def submit_new_password(self):
        global current_password
        old_password = self.old_password_entry.get() # Get input for old password
        new_password = self.new_password_entry.get() # Get input for new password
        
        # Check old passsowrd match or not 
        if old_password != current_password:
            messagebox.showerror("Error", "Old password is incorrect.") # Show error message
        else:
            if new_password:
                current_password = new_password
                self.save_password()  # Save the new password
                messagebox.showinfo("Success", "Password changed successfully!")
                self.change_password_window.destroy()  # Close the password change window
            else:
                messagebox.showerror("Error", "New password cannot be empty.") # Show error message and load the current password from the file

    # Create display tab for display all data
    def create_display_tab(self):
        self.display_frame = ttk.Frame(self.display_tab)
        self.display_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.display_frame, columns=("ID", "Name", "Age", "Description"), show='headings')
        self.tree.heading("ID", text="Patient ID")
        self.tree.heading("Name", text="Patient Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Description", text="Description")
        self.tree.pack(fill="both", expand=True)

        self.refresh_button = ttk.Button(self.display_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack(pady=10)

        self.export_button = ttk.Button(self.display_frame, text="Export All Data to PDF", command=self.export_all_data_to_pdf)
        self.export_button.pack(pady=10)
     
    # Function to refresh the data   
    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for patient_id, info in patients.items():
            self.tree.insert("", "end", values=(patient_id, info['name'], info['age'], info['description']))

    # Function to export as a pdf file using reportlab
    def export_all_data_to_pdf(self):
        if not patients:
            messagebox.showwarning("Warning", "No data to export.") # Show error message ,when no data to export
            return

        pdf_file_name = "Patients_data_by_HMMSystem_Admin.pdf" # Set file name to the pdf file
        c = canvas.Canvas(pdf_file_name, pagesize=letter)
        c.drawString(100, 750, "Patients Records") # Give a title name
        c.drawString(100, 730, "===================") # Seperate symbols

        y_position = 710 # Set height position
        for patient_id, info in patients.items():
            c.drawString(100, y_position, f"ID: {patient_id}, Name: {info['name']}, Age: {info['age']}, Description: {info['description']}")
            y_position -= 20  # Move down for the next entry

            if y_position < 50:  # Check if we need to create a new page
                c.showPage()
                y_position = 750  # Reset y position for new page

        c.save() # Save pdf file
        messagebox.showinfo("Success", f"Exported all data to {pdf_file_name}.") # Show a message after the save pdf file
    
    # Create a tab for Update Status
    def create_updateStatus_tab(self):
        self.updateStatus_frame = ttk.Frame(self.updateStatus_tab)
        self.updateStatus_frame.pack(fill="both", expand=True)

        # Get patient ID
        self.updateStatus_id_label = ttk.Label(self.updateStatus_frame, text="Patient ID: ")
        self.updateStatus_id_label.pack(pady=5)
        self.updateStatus_id_entry = ttk.Entry(self.updateStatus_frame)
        self.updateStatus_id_entry.pack(pady=5)

        # Get new data / informations
        self.updateStatus_description_label = ttk.Label(self.updateStatus_frame, text="Update Description:")
        self.updateStatus_description_label.pack(pady=5)
        self.updateStatus_description_entry = ttk.Entry(self.updateStatus_frame)
        self.updateStatus_description_entry.pack(pady=5)

        # Button to submit data
        self.updateStatus_button = ttk.Button(self.updateStatus_frame, text="Update Status", command=self.update_status)
        self.updateStatus_button.pack(pady=10)

    # Function to update status
    def update_status(self):
        patient_id = self.updateStatus_id_entry.get() # Get input from updateStatus Tab to Patient ID
        status = self.updateStatus_description_entry.get() # Get input from updateStatus Tab to update status

        if patient_id in patients: # Check patient_id in the dataset
            patients[patient_id]['description'] = status
            messagebox.showinfo("Success", f"Updated {patients[patient_id]['name']} (ID: {patient_id}) with new status.") # Show a message after the successfully updated data 
            self.save_data()  # Save the updated data
            self.clear_entries()  # Clear the entry fields
            self.refresh_data()  # Refresh the Display tab to show updated data
        else:
            messagebox.showerror("Error", "Invalid Patient ID") # Show an error message
    
    # Create a tab for Update All data
    def create_update_tab(self):
        self.update_frame = ttk.Frame(self.update_tab)
        self.update_frame.pack(fill="both", expand=True)

        self.id_label = ttk.Label(self.update_frame, text="Patient ID:")
        self.id_label.pack(pady=5)
        self.id_entry = ttk.Entry(self.update_frame)
        self.id_entry.pack(pady=5)

        self.name_label = ttk.Label(self.update_frame, text="Patient Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.update_frame)
        self.name_entry.pack(pady=5)

        self.age_label = ttk.Label(self.update_frame, text="Age:")
        self.age_label.pack(pady=5)
        self.age_entry = ttk.Entry(self.update_frame)
        self.age_entry.pack(pady=5)

        self.description_label = ttk.Label(self.update_frame, text="Description:")
        self.description_label.pack(pady=5)
        self.description_entry = ttk.Entry(self.update_frame)
        self.description_entry.pack(pady=5)

        self.add_button = ttk.Button(self.update_frame, text="Add Data", command=self.add_data)
        self.add_button.pack(pady=10)

        self.update_button = ttk.Button(self.update_frame, text="Update Data", command=self.update_data)
        self.update_button.pack(pady=10)

        self.delete_button = ttk.Button(self.update_frame, text="Delete Data", command=self.delete_data)
        self.delete_button.pack(pady=10)
        
    # Function for check age is valid or not ( input should be less than 100 and more than 0 )        
    def is_valid_age(self, age):
        #Check if the age is a valid two-digit number (0-99)
        return age.isdigit() and 0 <= int(age) <= 99

    # Function for add data into json dataset
    def add_data(self):
        # Get inputs for all fileds
        patient_id = self.id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        description = self.description_entry.get()

        # Check patient id and age is digit or not and whether age is valid or not
        if patient_id and name and age.isdigit() and self.is_valid_age(age):
            if patient_id in patients:
                # Show an error message ,when patient ID is already exists
                messagebox.showerror("Error", "Patient ID already exists. Please use a different ID.")
            else:
                patients[patient_id] = {"name": name, "age": int(age), "description": description}
                # Show a message after the succussfully added data
                messagebox.showinfo("Success", f"Added {name} with ID {patient_id} and age {age}.")
                self.save_data()  # Save data after adding
                self.clear_entries() # Clear entries
                self.refresh_data() # Refresh data
        else:
            # Show an error message, when ID or age wrong 
            messagebox.showerror("Error", "Please enter valid ID, name and age.")
    
    # Function for update data
    def update_data(self):
        # Get input for patient_ID
        patient_id = self.id_entry.get()
        # Check patient id in json dataset
        if patient_id in patients:
            # Get inputs for all fileds
            name = self.name_entry.get()
            age = self.age_entry.get()
            description = self.description_entry.get()
            
            # Check patient id and age is digit or not and whether age is valid or not
            if name and age.isdigit() and self.is_valid_age(age):
                patients[patient_id] = {"name": name, "age": int(age), "description": description}
                messagebox.showinfo("Success", f"Updated {patient_id} to {name} with age {age} and {description}.")
                self.save_data()  # Save data after updating
                self.clear_entries() # Clear entries
                self.refresh_data() # Refresh data
            else:
                messagebox.showerror("Error", "Please enter valid name, age and description.")
        else:
            messagebox.showerror("Error", "Patient ID not found.")
    
    # Function to delete the data from json dataset    
    def delete_data(self):
        # Get input for patient_id
        patient_id = self.id_entry.get()
        # Check patient id in the json dataset
        if patient_id in patients:
            del patients[patient_id] # Delete the all data from json dataset
            messagebox.showinfo("Success", f"Deleted data with ID {patient_id}.") # Show a message after deleted the data
            self.save_data()  # Save data after deleting
            self.clear_entries() # Clear entries
            self.refresh_data() # Refresh data
        else:
            messagebox.showerror("Error", "Patient ID not found.") # Show an error message ,when patient id not founded

    # Function to clear entries data
    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.check_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    # Function to save data
    def save_data(self):
        with open(data_file, 'w') as f:
            json.dump(patients, f)

    # Function to load json dataset
    def load_patients(self):
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                global patients
                patients = json.load(f)

    
    # Create a tab for check data
    def create_check_tab(self):
        self.check_frame = ttk.Frame(self.check_tab)
        self.check_frame.pack(fill="both", expand=True)

        self.check_label = ttk.Label(self.check_frame, text="Enter Patient ID to Check:")
        self.check_label.pack(pady=5)
        self.check_entry = ttk.Entry(self.check_frame)
        self.check_entry.pack(pady=5)

        self.check_button = ttk.Button(self.check_frame, text="Check Patient", command=self.check_data)
        self.check_button.pack(pady=10)

        self.search_label = ttk.Label(self.check_frame, text="Enter Search Term:")
        self.search_label.pack(pady=5)
        self.search_entry = ttk.Entry(self.check_frame)
        self.search_entry.pack(pady=5)

        self.search_button = ttk.Button(self.check_frame, text="Search Patient Data", command=self.search_data)
        self.search_button.pack(pady=10)
     
    # Function for check data   
    def check_data(self):
        patient_id = self.check_entry.get()
        if patient_id in patients:
            # Create a variable to assign patient id
            patient_info = patients[patient_id]
            # Display a message ,when Patient id found from the json datset
            messagebox.showinfo("Patient Found", f"ID: {patient_id}, Name: {patient_info['name']}, Age: {patient_info['age']}.")
        else:
            # Display a message , when Patient ID didn't found
            messagebox.showerror("Error", "Patient ID not found.")

    # Function for search data
    def search_data(self):
        # Get input for search term
        search_term = self.search_entry.get()
        # Assign a variable to get all data
        results = [patient_id for patient_id, info in patients.items() if search_term.lower() in info['name'].lower()]
        if results:
            # Show a message ,when data found
            messagebox.showinfo("Search Results", "Found: " + ", ".join(results))
        else:
            # Show an error message data not found
            messagebox.showinfo("Search Results", "No Patient found.")


    # Create a tab for about
    def create_about_tab(self):
        self.about_frame = ttk.Frame(self.about_tab)
        self.about_frame.pack(fill="both", expand=True)
        
        # Label to show about section data
        about_label = ttk.Label(self.about_frame, text="Hospital Medicine Management System - Admin\nDeveloped by: Vihanga Anuththara\nFollow me on GitHub: vanu888\nPower to FOSS :)", font=("Arial", 12))
        about_label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially
    app = HospitalMedicineManagementAdminApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import json
import os

# Sample data structure to hold medicines records
medicines = {}
current_password = "password"  # current password
password_file = "current_password.json"  # File to store the current password
data_file = "medicines.json"  # File to store medicines data using json

#Create main application
class HospitalMedicineManagementApp:
    def __init__(self, root):
        self.root = root # Main window name as root
        self.root.title("Hospital Medicine Management System") # Main title
        self.root.geometry("800x600") # Window frame size
        
        # Load password file
        self.load_password()
        # Load saved medicines data
        self.load_medicines()
        

        # Create style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial",12))
        self.style.configure("TEntry", background="#ffffff", font=("Arial",12))
        self.style.configure("TButton", background="#4CAF50", foreground="white", font=("Arial",12, "bold"))
        self.style.map("TButton", background=[("active", "#45a049")])
        self.style.configure("TNotebook", padding=[5,5])
        self.style.configure("TNotebook.Tab", padding=[15,8], font=("Arial",12,"bold"))

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        self.login_tab = ttk.Frame(self.notebook)
        self.medicine_tab = ttk.Frame(self.notebook)
        self.display_tab = ttk.Frame(self.notebook)
        self.issue_tab = ttk.Frame(self.notebook)
        self.check_tab = ttk.Frame(self.notebook)
        self.chart_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.login_tab, text="Login")
        self.notebook.add(self.display_tab, text="Display Medicines")
        self.notebook.add(self.issue_tab, text="Issue Medicines")
        self.notebook.add(self.medicine_tab, text="Medicines")
        self.notebook.add(self.check_tab, text="Check") 
        self.notebook.add(self.chart_tab, text="Chart")
        self.notebook.add(self.about_tab, text="About")

        self.create_login_tab()
        self.create_medicine_tab()
        self.create_display_tab()
        self.create_issue_tab()
        self.create_check_tab()
        self.create_chart_tab()
        self.create_about_tab()

        # disable all tabs except login
        self.lock_tabs()

        # Show welcome screen
        self.show_welcome_screen()


    def show_welcome_screen(self):
        # Create a new window for the welcome screen
        self.welcome_window = tk.Toplevel(self.root)
        self.welcome_window.title("Hospital Medicine Management System")
        self.welcome_window.geometry("800x600")
        self.welcome_window.configure(bg="#f0f0f0")

        # Create a loading label
        loading_label = ttk.Label(self.welcome_window, text="Loading, please wait...", background="#f0f0f0")
        loading_label.pack(pady=20)

        # Create a loading bar
        self.loading_bar = ttk.Progressbar(self.welcome_window, orient="horizontal", length=300, mode="indeterminate")
        self.loading_bar.pack(pady=10)
        self.loading_bar.start()  # Start the loading animation

        # Close the welcome window after 5 seconds
        self.welcome_window.after(5000, self.close_welcome_screen)

    def close_welcome_screen(self):
        self.loading_bar.stop()  # Stop the loading animation
        self.welcome_window.destroy()  # Close the welcome window
        self.root.deiconify()  # Show the main application window
        self.notebook.select(self.login_tab)  # Switch to the login tab
        
        
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
    
    # Function to lock tabs
    def lock_tabs(self):
        for i in range(1, 7):  # Disable all tabs except the first (login)
            self.notebook.tab(i, state='disabled')

    # Function to unlock tabs
    def unlock_tabs(self):
        for i in range(1, 7):  # Enable all tabs except the first (login)
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
    
    # Create display tab for show saved data
    def create_display_tab(self):
        self.display_frame = ttk.Frame(self.display_tab)
        self.display_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.display_frame, columns=("ID", "Name", "Quantity", "Supplier"), show='headings')
        self.tree.heading("ID", text="Medicine ID")
        self.tree.heading("Name", text="Medicine Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.pack(fill="both", expand=True)

        self.refresh_button = ttk.Button(self.display_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack(pady=10)

        self.export_button = ttk.Button(self.display_frame, text="Export All Data", command=self.export_all_data_to_pdf)
        self.export_button.pack(pady=10)
     
    # Function for refresh the data   
    def refresh_data(self):
        # Clear the tree view
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert updated data
        for med_id, info in medicines.items():
            self.tree.insert("", "end", values=(med_id, info['name'], info['quantity'], info['supplier']))

    # Function for export data as a pdf
    def export_all_data_to_pdf(self):
        if not medicines:
            messagebox.showwarning("Warning", "No data to export.")
            return

        pdf_file_name = "Medcines data by HMMSystem.pdf" # Create a variable to assign pdf name
        c = canvas.Canvas(pdf_file_name, pagesize=letter)
        c.drawString(100, 750, "Medicines Records")
        c.drawString(100, 730, "===================")

        y_position = 710
        for med_id, info in medicines.items():
            c.drawString(100, y_position, f"ID: {med_id}, Name: {info['name']}, Quantity: {info['quantity']}, Supplier: {info['supplier']}")
            y_position -= 20  # Move down for the next entry

            if y_position < 50:  # Check if we need to create a new page
                c.showPage()
                y_position = 750  # Reset y position for new page

        c.save()
        messagebox.showinfo("Success", f"Exported all data to {pdf_file_name}.") # Show a succuss message       
        
    # Create Issue medicines tab
    def create_issue_tab(self):
        self.issue_frame = ttk.Frame(self.issue_tab)
        self.issue_frame.pack(fill="both", expand=True)

        self.issue_id_label = ttk.Label(self.issue_frame, text= "Medicine ID: ")
        self.issue_id_label.pack(pady=5)
        self.issue_id_entry = ttk.Entry(self.issue_frame)
        self.issue_id_entry.pack(pady=5)

        self.issue_quantity_label = ttk.Label(self.issue_frame, text="Quantity to issue: ")
        self.issue_quantity_label.pack(pady=5)
        self.issue_quantity_entry = ttk.Entry(self.issue_frame)
        self.issue_quantity_entry.pack(pady=5)

        #button to submit update data
        self.issue_button = ttk.Button(self.issue_frame, text="Issue medicines", command=self.issue_medicines)
        self.issue_button.pack(pady=10)

    #Function for Issue medicines -- 24.09.2024 (Bosco sir)
    def issue_medicines(self):
        med_id = self.issue_id_entry.get()
        quantity_to_issue = self.issue_quantity_entry.get()

        #Check if stores have enough quantity or not
        if med_id in medicines and quantity_to_issue.isdigit():
            quantity_to_issue = int(quantity_to_issue)
            current_quantity = medicines[med_id]['quantity']
            
            # Check whether stores have enough quantity or not
            if quantity_to_issue > current_quantity:
                messagebox.showerror("Warning","Not enough quantity available to issue!")
            else:
                medicines[med_id]['quantity'] -= quantity_to_issue # Issue the quantity
                messagebox.showinfo("Success", f"Issued {quantity_to_issue} of {medicines [med_id]['name']} (ID: {med_id})")

                self.save_medicines() #Save the updated data
                self.clear_entries() #Clear the entry fields
                self.refresh_data() #Refresh the Display tab to show updated quantities
        else:
            messagebox.showerror("Error","Invalid medicine ID or quantity") # Show an error message
    

    # Create medicine tab
    def create_medicine_tab(self):
        self.medicine_frame = ttk.Frame(self.medicine_tab)
        self.medicine_frame.pack(fill="both", expand=True)

        self.id_label = ttk.Label(self.medicine_frame, text="Medicine ID:")
        self.id_label.pack(pady=5)
        self.id_entry = ttk.Entry(self.medicine_frame)
        self.id_entry.pack(pady=5)

        self.name_label = ttk.Label(self.medicine_frame, text="Medicine Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self.medicine_frame)
        self.name_entry.pack(pady=5)

        self.quantity_label = ttk.Label(self.medicine_frame, text="Quantity:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ttk.Entry(self.medicine_frame)
        self.quantity_entry.pack(pady=5)

        self.supplier_label = ttk.Label(self.medicine_frame, text="Supplier:")
        self.supplier_label.pack(pady=5)
        self.supplier_entry = ttk.Entry(self.medicine_frame)
        self.supplier_entry.pack(pady=5)

        self.add_button = ttk.Button(self.medicine_frame, text="Add Medicine", command=self.add_medicine)
        self.add_button.pack(pady=10)

        self.update_button = ttk.Button(self.medicine_frame, text="Update Medicine", command=self.update_medicine)
        self.update_button.pack(pady=10)

        self.delete_button = ttk.Button(self.medicine_frame, text="Delete Medicine", command=self.delete_medicine)
        self.delete_button.pack(pady=10)
    
    # Function for add medicines
    def add_medicine(self):
        med_id = self.id_entry.get()
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        supplier = self.supplier_entry.get()

        if med_id and name and quantity.isdigit():
            if med_id in medicines:
                messagebox.showerror("Error", "Medicine ID already exists. Please use a different ID.")
            else:
                medicines[med_id] = {"name": name, "quantity": int(quantity), "supplier": supplier}
                messagebox.showinfo("Success", f"Added {name} with ID {med_id} and quantity {quantity}.")
                self.save_medicines()  # Save medicines after adding
                self.clear_entries()
                self.refresh_data()
        else:
            messagebox.showerror("Error", "Please enter valid ID, name, quantity and a supplier.")

    # Function for update medicine data
    def update_medicine(self):
        med_id = self.id_entry.get()
        if med_id in medicines:
            name = self.name_entry.get()
            quantity = self.quantity_entry.get()
            supplier = self.supplier_entry.get()
            if name and quantity.isdigit():
                medicines[med_id] = {"name": name, "quantity": int(quantity), "supplier": supplier}
                messagebox.showinfo("Success", f"Updated {med_id} to {name} with quantity {quantity} and {supplier}.")
                self.save_medicines()  # Save medicines after updating
                self.clear_entries()
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Please enter valid name, quantity and supplier.")
        else:
            messagebox.showerror("Error", "Medicines ID not found.")

    # Function for delete medicine data
    def delete_medicine(self):
        med_id = self.id_entry.get()
        if med_id in medicines:
            del medicines[med_id]
            messagebox.showinfo("Success", f"Deleted medicine with ID {med_id}.")
            self.save_medicines()  # Save medicines after deleting
            self.clear_entries()
            self.refresh_data()
        else:
            messagebox.showerror("Error", "Medicine ID not found.")
    
    # Function for Clear entries        
    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.supplier_entry.delete(0, tk.END)
        self.check_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    # Function for save data
    def save_medicines(self):
        with open(data_file, 'w') as f:
            json.dump(medicines, f)

    # Function for load json dataset
    def load_medicines(self):
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                global medicines
                medicines = json.load(f)

    # Create checking tab for search and check data
    def create_check_tab(self):
        self.check_frame = ttk.Frame(self.check_tab)
        self.check_frame.pack(fill="both", expand=True)

        # Check Medicine Section
        self.check_label = ttk.Label(self.check_frame, text="Enter Medicine ID to Check:")
        self.check_label.pack(pady=5)
        self.check_entry = ttk.Entry(self.check_frame)
        self.check_entry.pack(pady=5)

        self.check_button = ttk.Button(self.check_frame, text="Check Medicine", command=self.check_medicine)
        self.check_button.pack(pady=10)

        # Search Medicine Section
        self.search_label = ttk.Label(self.check_frame, text="Enter Search Term:")
        self.search_label.pack(pady=5)
        self.search_entry = ttk.Entry(self.check_frame)
        self.search_entry.pack(pady=5)

        self.search_button = ttk.Button(self.check_frame, text="Search Medicine", command=self.search_medicine)
        self.search_button.pack(pady=10)
     
    # Function for check medicine data using ID 
    def check_medicine(self):
        med_id = self.check_entry.get()
        if med_id in medicines:
            med_info = medicines[med_id]
            messagebox.showinfo("Medicine Found", f"ID: {med_id}, Name: {med_info['name']}, Quantity: {med_info['quantity']}.")
        else:
            messagebox.showerror("Error", "Medicine ID not found.")

    # Function for search medicine using a term
    def search_medicine(self):
        search_term = self.search_entry.get()
        results = [med_id for med_id, info in medicines.items() if search_term.lower() in info['name'].lower()]
        if results:
            messagebox.showinfo("Search Results", "Found: " + ", ".join(results))
        else:
            messagebox.showinfo("Search Results", "No medicines found.")

    # Create chart tab
    def create_chart_tab(self):
        self.chart_frame = ttk.Frame(self.chart_tab)
        self.chart_frame.pack(fill="both", expand=True)
        self.company_label = ttk.Label(self.chart_frame, text="Enter supplier:")
        self.company_label.pack(pady=5)
        self.company_entry = ttk.Entry(self.chart_frame)
        self.company_entry.pack(pady=5)
        self.plot_button = ttk.Button(self.chart_frame, text="Graph Medicines Data", command=self.plot_medicine_data)
        self.plot_button.pack(pady=10)
        
    # Function to plot medicines data   
    def plot_medicine_data(self):
        supplier_name = self.company_entry.get()
        if not supplier_name:
            messagebox.showwarning("Warning", "Please enter a supplier name!")
            return

        # Filter medicines by supplier
        filtered_medicines = {med_id: info for med_id, info in medicines.items() if info['supplier'] == supplier_name}
        
        if not filtered_medicines:
            messagebox.showwarning("Warning", "No medicines found for this supplier!")
            return

        names = [info['name'] for info in filtered_medicines.values()]  # Take names
        quantities = [info['quantity'] for info in filtered_medicines.values()]  # Take quantities

        plt.figure(figsize=(10, 6))
        plt.bar(names, quantities, color='skyblue')  # Draw bar graph
        plt.xlabel('Medicine Name')  # X Label name
        plt.ylabel('Quantity')  # Y Label name
        plt.title(f'Medicines from Supplier: {supplier_name}')  # Graph title
        plt.xticks(rotation=45)  # Rotate
        plt.tight_layout()
        plt.show()  # Show the graph
  
    # Create about section tab
    def create_about_tab(self):
        self.about_frame = ttk.Frame(self.about_tab)
        self.about_frame.pack(fill="both", expand=True)
        # About section data
        about_label = ttk.Label(self.about_frame, text="Hospital Medicine Management System\nDeveloped by: Vihanga Anuththara \nFollow me on Github: vanu888 \npower to FOSS :)")
        about_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially
    app = HospitalMedicineManagementApp(root)
    root.mainloop()
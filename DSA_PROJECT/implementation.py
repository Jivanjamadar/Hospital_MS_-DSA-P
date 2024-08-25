# Hospital Management System (HMS)

class Patient:
    def __init__(self, patient_id, name, age, medical_history):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.medical_history = medical_history

class TreeNode:
    def __init__(self, patient):
        self.patient = patient
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, patient):
        if not root:
            return TreeNode(patient)
        elif patient.patient_id < root.patient.patient_id:
            root.left = self.insert(root.left, patient)
        else:
            root.right = self.insert(root.right, patient)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and patient.patient_id < root.left.patient.patient_id:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and patient.patient_id > root.right.patient.patient_id:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and patient.patient_id > root.left.patient.patient_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and patient.patient_id < root.right.patient.patient_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, patient_id):
        if not root:
            return root

        if patient_id < root.patient.patient_id:
            root.left = self.delete(root.left, patient_id)
        elif patient_id > root.patient.patient_id:
            root.right = self.delete(root.right, patient_id)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.patient = temp.patient
            root.right = self.delete(root.right, temp.patient.patient_id)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def search(self, root, patient_id):
        if not root or root.patient.patient_id == patient_id:
            return root
        if patient_id < root.patient.patient_id:
            return self.search(root.left, patient_id)
        return self.search(root.right, patient_id)

    def in_order(self, root):
        res = []
        if root:
            res = self.in_order(root.left)
            res.append(root.patient)
            res = res + self.in_order(root.right)
        return res

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def get_all(self):
        return self.items[:]

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def get_all(self):
        return self.items[:]

class HospitalManagementSystem:
    def __init__(self):
        self.avl = AVLTree()
        self.appointment_queue = Queue()
        self.emergency_stack = Stack()

    def register_patient(self, patient):
        self.avl.root = self.avl.insert(self.avl.root, patient)
        print(f"\n-> Patient '{patient.name}' registered successfully.")

    def check_in_patient(self, patient):
        self.register_patient(patient)

    def check_out_patient(self, patient_id):
        self.avl.root = self.avl.delete(self.avl.root, patient_id)
        print(f"Patient with ID '{patient_id}' checked out successfully.")

    def schedule_appointment(self, patient):
        self.avl.root = self.avl.insert(self.avl.root, patient)
        self.appointment_queue.enqueue(patient)
        print(f"Appointment scheduled for patient '{patient.name}'.")

    def handle_emergency(self, patient):
        self.avl.root = self.avl.insert(self.avl.root, patient)
        self.emergency_stack.push(patient)
        print(f"Emergency case handled for patient '{patient.name}'.")

    def get_next_appointment(self):
        patient = self.appointment_queue.dequeue()
        if patient:
            print(f"Next appointment: {patient.name} - {patient.medical_history}")
        else:
            print("No appointments scheduled.")
        return patient

    def get_next_emergency(self):
        patient = self.emergency_stack.pop()
        if patient:
            print(f"Next emergency: {patient.name} - {patient.medical_history}")
        else:
            print("No emergency cases.")
        return patient

    def search_patient(self, patient_id):
        patient_node = self.avl.search(self.avl.root, patient_id)
        if patient_node:
            patient = patient_node.patient
            print(f"Patient found: {patient.name} - {patient.medical_history}")
        else:
            print("Patient not found.")
        return patient_node

    def list_all_patients_in_avl(self):
        patients = self.avl.in_order(self.avl.root)
        if patients:
            print("Patients in AVL Tree:")
            for patient in patients:
                print(f"\nID: {patient.patient_id},\n Name: {patient.name},\n Age: {patient.age},\n Medical History: {patient.medical_history}")
        else:
            print("\nNo patients in AVL Tree.")

    def list_all_appointments(self):
        patients = self.appointment_queue.get_all()
        if patients:
            print("Appointments Queue:")
            for patient in patients:
                print(f"\nID: {patient.patient_id},\n Name: {patient.name},\n Age: {patient.age},\n Medical History: {patient.medical_history}")
        else:
            print("No patients in appointment queue.")

    def list_all_emergency_cases(self):
        patients = self.emergency_stack.get_all()
        if patients:
            print("Emergency Stack:")
            for patient in patients:
                print(f"\nID: {patient.patient_id},\n Name: {patient.name},\n Age: {patient.age},\n Medical History: {patient.medical_history}")
        else:
            print("No emergency cases in stack.")

def main():
    hms = HospitalManagementSystem()
    
    while True:
        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
        print("Hospital Management System Menu")
        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")

        print("1. Register a new patient")
        print("2. Check-in a patient")
        print("3. Check-out a patient")
        print("4. Schedule an appointment")
        print("5. Handle an emergency case")
        print("6. Get next appointment")
        print("7. Get next emergency case")
        print("8. Search for a patient by ID")
        print("9. List all patients in AVL tree")
        print("10. List all appointments in queue")
        print("11. List all emergency cases in stack")
        print("12. Exit")
        print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")

        choice = input("Enter your choice (1-12): ")
        print("________________Response !____________________________")

        if choice == '1':
            patient_id = int(input("Enter Patient ID: "))
            name = input("Enter Patient Name: ")
            age = int(input("Enter Patient Age: "))
            medical_history = input("Enter Medical History: ")
            patient = Patient(patient_id, name, age, medical_history)
            hms.register_patient(patient)

        elif choice == '2':
            patient_id = int(input("Enter Patient ID: "))
            name = input("Enter Patient Name: ")
            age = int(input("Enter Patient Age: "))
            medical_history = input("Enter Medical History: ")
            patient = Patient(patient_id, name, age, medical_history)
            hms.check_in_patient(patient)

        elif choice == '3':
            patient_id = int(input("Enter Patient ID to check out: "))
            hms.check_out_patient(patient_id)

        elif choice == '4':
            patient_id = int(input("Enter Patient ID: "))
            name = input("Enter Patient Name: ")
            age = int(input("Enter Patient Age: "))
            medical_history = input("Enter Medical History: ")
            patient = Patient(patient_id, name, age, medical_history)
            hms.schedule_appointment(patient)

        elif choice == '5':
            patient_id = int(input("Enter Patient ID: "))
            name = input("Enter Patient Name: ")
            age = int(input("Enter Patient Age: "))
            medical_history = input("Enter Medical History: ")
            patient = Patient(patient_id, name, age, medical_history)
            hms.handle_emergency(patient)

        elif choice == '6':
            hms.get_next_appointment()

        elif choice == '7':
            hms.get_next_emergency()

        elif choice == '8':
            patient_id = int(input("Enter Patient ID to search: "))
            hms.search_patient(patient_id)

        elif choice == '9':
            hms.list_all_patients_in_avl()

        elif choice == '10':
            hms.list_all_appointments()

        elif choice == '11':
            hms.list_all_emergency_cases()

        elif choice == '12':
            print("Exiting the system. Be healthy !")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

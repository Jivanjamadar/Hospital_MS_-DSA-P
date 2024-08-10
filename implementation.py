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

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, patient):
        if not root:
            return TreeNode(patient)
        elif patient.patient_id < root.patient.patient_id:
            root.left = self.insert(root.left, patient)
        else:
            root.right = self.insert(root.right, patient)
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
        return root

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

class AVLTree(BST):
    def insert(self, root, patient):
        root = super().insert(root, patient)
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)
        if balance > 1 and patient.patient_id < root.left.patient.patient_id:
            return self.right_rotate(root)
        if balance < -1 and patient.patient_id > root.right.patient.patient_id:
            return self.left_rotate(root)
        if balance > 1 and patient.patient_id > root.left.patient.patient_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and patient.patient_id < root.right.patient.patient_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def delete(self, root, patient_id):
        root = super().delete(root, patient_id)
        if not root:
            return root
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
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

class HospitalManagementSystem:
    def __init__(self):
        self.bst = BST()
        self.avl = AVLTree()
        self.appointment_queue = Queue()
        self.emergency_stack = Stack()

    def register_patient(self, patient):
        self.bst.root = self.bst.insert(self.bst.root, patient)
        self.avl.root = self.avl.insert(self.avl.root, patient)

    def check_in_patient(self, patient):
        self.register_patient(patient)

    def check_out_patient(self, patient_id):
        self.bst.root = self.bst.delete(self.bst.root, patient_id)
        self.avl.root = self.avl.delete(self.avl.root, patient_id)

    def schedule_appointment(self, patient):
        self.appointment_queue.enqueue(patient)

    def handle_emergency(self, patient):
        self.emergency_stack.push(patient)

    def get_next_appointment(self):
        return self.appointment_queue.dequeue()

    def get_next_emergency(self):
        return self.emergency_stack.pop()

    def search_patient(self, patient_id):
        return self.bst.search(self.bst.root, patient_id) or self.avl.search(self.avl.root, patient_id)

# Testing program with example
if __name__ == "__main__":
    hms = HospitalManagementSystem()
    
    # Register patients
    hms.register_patient(Patient(1, "John Doe", 30, "Flu"))
    hms.register_patient(Patient(2, "Jane Smith", 25, "Cough"))
    hms.register_patient(Patient(3, "Alice Johnson", 40, "Fever"))

    # Schedule appointments
    hms.schedule_appointment(Patient(4, "Bob Brown", 35, "Headache"))
    hms.schedule_appointment(Patient(5, "Charlie Davis", 50, "Back Pain"))

    # Handle emergency
    hms.handle_emergency(Patient(6, "Diana Evans", 60, "Heart Attack"))

    # Get next appointment
    next_appointment = hms.get_next_appointment()
    print(f"Next appointment: {next_appointment.name} - {next_appointment.medical_history}")

    # Get next emergency
    next_emergency = hms.get_next_emergency()
    print(f"Next emergency: {next_emergency.name} - {next_emergency.medical_history}")

    # Search for a patient
    patient = hms.search_patient(2)
    if patient:
        print(f"Patient found: {patient.patient.name} - {patient.patient.medical_history}")
    else:
        print("Patient not found")

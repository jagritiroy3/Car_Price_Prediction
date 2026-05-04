from tkinter import *
import pickle
from PIL import Image, ImageTk

# ===== Format Function =====
def format_value(value):
    if value >= 10000000:
        return f"{value/10000000:.2f} Cr"
    elif value >= 100000:
        return f"{value/100000:.2f} Lakhs"
    else:
        return str(value)

# ===== Load Model =====
with open('./saved_models/RandomForestRegressor.pkl', 'rb') as f:
    model = pickle.load(f)

with open('./saved_scaling/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

seller_selected_value = "Dealer"
fuel_selected_value = "Petrol"
transmission_selected_value = "Manual"

# ===== Prediction Function =====
def pred_price():
    try:
        input_values = []

        car_name = car_name_entry.get()

        input_values.append(int(vehicle_age_entry.get()))
        input_values.append(int(km_driven_entry.get()))
        input_values.append(float(mileage_entry.get()))
        input_values.append(int(engine_entry.get()))
        input_values.append(float(max_power_entry.get()))
        input_values.append(int(seats_entry.get()))

        if seller_selected_value == "Dealer":
            input_values.extend([1, 0, 0])
        elif seller_selected_value == "Individual":
            input_values.extend([0, 1, 0])
        else:
            input_values.extend([0, 0, 1])

        fuel_dict = {
            "CNG":[1,0,0,0,0],
            "Diesel":[0,1,0,0,0],
            "Electric":[0,0,1,0,0],
            "LPG":[0,0,0,1,0],
            "Petrol":[0,0,0,0,1]
        }
        input_values.extend(fuel_dict[fuel_selected_value])

        if transmission_selected_value == "Automatic":
            input_values.extend([1,0])
        else:
            input_values.extend([0,1])

        input_scaled = scaler.transform([input_values])
        prediction = model.predict(input_scaled)[0]
        prediction = format_value(prediction)

        price_label.config(text=f"{car_name} → ₹ {prediction}")

    except:
        price_label.config(text="Invalid Input")

# ===== UI =====
root = Tk()
root.title("Car Price Predictor")
root.geometry("1700x900")

# ===== Background Image =====
img = Image.open(r"C:\Car pricing Prediction\App\car.jpeg")
img = img.resize((1700, 900))
bg_image = ImageTk.PhotoImage(img)

bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ===== Title =====
title = Label(root, text="🚗 Car Price Prediction",
              bg="#1e1e2f", fg="#9E0606",
              font=("Helvetica", 45, "bold"))
title.place(relx=0.5, y=40, anchor="center")

# ===== MAIN FRAME (LEFT SIDE 👈 IMPORTANT CHANGE) =====
main_frame = Frame(root, bg="#222233")
main_frame.place(relx=0, rely=0.5, anchor="w")   # 👈 YE LINE IMPORTANT HAI

# ===== Input Fields =====
def create_field(row, text):
    Label(main_frame, text=text,
          bg="#222233", fg="white",
          font=("Helvetica", 13)).grid(row=row, column=0, padx=30, pady=15, sticky="w")
    
    entry = Entry(main_frame,
                  font=("Helvetica", 13),
                  width=20,
                  
                  bg="#2c2c3c",
                  fg="white",
                  insertbackground="white",
                  relief=FLAT)
    entry.grid(row=row, column=1, pady=10)
    return entry

car_name_entry = create_field(0, "Car Name")
vehicle_age_entry = create_field(1, "Vehicle Age")
km_driven_entry = create_field(2, "KM Driven")
mileage_entry = create_field(3, "Mileage")
engine_entry = create_field(4, "Engine (CC)")
max_power_entry = create_field(5, "Max Power")
seats_entry = create_field(6, "Seats")

# ===== Dropdowns =====
def dropdown(row, label, options, var):
    Label(main_frame, text=label,
          bg="#222233", fg="white",
          font=("Helvetica", 13)).grid(row=row, column=2, padx=20)
    
    menu = OptionMenu(main_frame, var, *options)
    menu.config(bg="#2c2c3c", fg="white", font=("Helvetica", 11))
    menu.grid(row=row, column=3)

seller_var = StringVar(value="Dealer")
fuel_var = StringVar(value="Petrol")
trans_var = StringVar(value="Manual")

dropdown(1, "Seller", ["Dealer","Individual","Trustmark Dealer"], seller_var)
dropdown(2, "Fuel", ["Petrol","Diesel","CNG","Electric","LPG"], fuel_var)
dropdown(3, "Transmission", ["Manual","Automatic"], trans_var)

def update_values(*args):
    global seller_selected_value, fuel_selected_value, transmission_selected_value
    seller_selected_value = seller_var.get()
    fuel_selected_value = fuel_var.get()
    transmission_selected_value = trans_var.get()

seller_var.trace("w", update_values)
fuel_var.trace("w", update_values)
trans_var.trace("w", update_values)

# ===== Button =====
btn = Button(root, text="Predict Price",
             command=pred_price,
             bg="#9E0606", fg="black",
             activebackground="#e60000",
             font=("Helvetica", 16, "bold"),
             bd=0,
             padx=30, pady=12)
btn.place(relx=0.1, rely=0.8, anchor="w")   

# ===== Output =====
price_label = Label(root, text="₹ 0",
                    bg="#222233", fg="white",
                    font=("Helvetica", 24, "bold"))
price_label.place(relx=0.15, rely=0.9, anchor="w")  

root.mainloop()
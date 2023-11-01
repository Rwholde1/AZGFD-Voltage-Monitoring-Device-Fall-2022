import pandas as pd
import random
from datetime import datetime, timedelta
import openpyxl

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

dates = []  # Changed variable name to 'dates'
times = []  # Changed variable name to 'times'
frequencies = []
voltages = []

for _ in range(10):
    # Generate a random date within the specified range
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    # Append the random date to the date_list
    dates.append(random_date.date())

    # Generate a random time
    random_time = datetime.strptime(
        f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}", "%H:%M:%S"
    )

    # Append the random time to the time_list
    times.append(random_time.time())
    
    frequency = random.randint(0,50)
    voltage = random.randint(0,50)
    voltages.append(voltage)
    frequencies.append(frequency)
    

print("Generated Dates:")
for d in dates:
    print(d.strftime("%Y-%m-%d"))

print("\nGenerated Times:")
for t in times:
    print(t.strftime("%H:%M:%S"))



filename = 'date.xlsx'
def write_to_execl(dates, times,voltages,frequencies, filename):  # Changed parameters to 'dates' and 'times'
    df = pd.DataFrame({
        'Date': dates,
        'Time': times,
        'Voltage' : voltages,
        'Frequency': frequencies
        
    })

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="DateAndTime", index=False)

write_to_execl(dates, times,voltages,frequencies, filename)

import calendar
import datetime as dt

class time_slot:
    #start_slot should be in dt.datetime(2026, 11, 6, 13, 29, 43, 79043) format
    #                                    yyyy, mm, dd, h, ss, ms, timezone
    def __init__(self, st_slt, end_slt):
        self.start_slot = st_slt
        self.end_slot = end_slt
    
    def __str__(self):
        return f"appointment {self.start_slot},ends at {self.end_slot}"
    
    def overlaps(self, other):
        condition_1 = self.start_slot < other.end_slot and other.start_slot < self.end_slot
        condition_2 = other.start_slot < self.end_slot and other.start_slot > self.end_slot
        return condition_1 or condition_2

#Vom folosi datele in format datetime -> pentru Google trebuie javascript :.(

class Planificator:
    current_date = dt.date(2026,1,1) # start at 2026.01.01

    WORK_START = dt.time(9, 30)
    WORK_END = dt.time(16, 30)

    def __init__(self):
        self.WORK_START = dt.datetime(2026, 11, 6, 9, 30)
        self.WORK_END = dt.datetime(2026, 11, 6, 16, 30) # le las aici ca sa citeasca din fisierul de input ulterior

        timeslot = time_slot(self.WORK_START, self.WORK_END)
        self.events =[]

    def __str__(self):
        return f"D {self.WORK_START} and {self.WORK_END}."

    def add_appointment(self, start, end):
        appointment = time_slot(start, end)
        
        isGoodAppointment = True

        for evt in self.events:
            duration_in = evt.start_slot - self.WORK_START
            duration_out =  self.WORK_END - evt.end_slot
            print (f"From work start {duration_in}, and to work end {duration_out}")

            if evt.overlaps(appointment):
                isGoodAppointment = False
                print(f"Overlaps with {evt}")
                # raise ValueError(f"Overlaps with {evt}")
                
        if start.time() < self.WORK_START.time() or end.time() > self.WORK_END.time():
            print("Rezervarea e in afara orelor de lucru")
            isGoodAppointment = False

        if isGoodAppointment:
            self.events.append(appointment)



    def show_appointments(self):
        for evt in self.events:
            print( f"One appointment: {evt.start_slot} - {evt.end_slot}" )

    def free_time(self):
        empty_slots = []

        apps = sorted(self.events, key = lambda events : events.start_slot)

        current = self.WORK_START

        print(f"+++++++Free Schedule+++++++")
        for evt in apps:
            if current < evt.start_slot:
                empty_slots.append(time_slot(current, evt.end_slot))
                print( f"Liber:{current} - {evt.start_slot}")
            current = max(evt.end_slot, current)
            
        if current < self.WORK_END:
            empty_slots.append(time_slot(current, self.WORK_END)) 
            print( f"Muncesti pentru Bolojan:{current} - {self.WORK_END}")
        
        return empty_slots



plnif = Planificator()

time1 = dt.datetime(2026, 11, 6, 10, 29, 43)
time2 = dt.datetime(2026, 11, 6, 11, 24, 43)

time3 = dt.datetime(2026, 11, 6, 13, 45, 43)
time4 = dt.datetime(2026, 11, 6, 16, 24, 43)

time5 = dt.datetime(2026, 11, 6, 12, 29, 43)
time6 = dt.datetime(2026, 11, 6, 13, 24, 43)



plnif.add_appointment( time1, time2 )

plnif.add_appointment( time3, time4 )

plnif.add_appointment( time5, time6 )


# print(plnif)

plnif.show_appointments()

plnif.free_time()

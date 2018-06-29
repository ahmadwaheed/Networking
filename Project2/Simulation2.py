# This is a simpy based  simulation of a M/M/1 queue system

import random
import simpy
import math
import matplotlib.pyplot as SimPlot

RANDOM_SEED = 29
SIM_TIME = 1000000
SLOT_PER_RATE = 1
SLOT_NUMBER = 0
HOST_NUMBERS = 10

class Ethernet_Simulation:
    def __init__(self, env, host_queue_line , slot_timing):
        self.env = env
        self.total_hosts = host_queue_line
        self.packets_processed = 0 #total no.of processed packets
        self.collisions = 0 #no.of slots collide
        self.slot_timing = slot_timing

        #Adding total number of hosts into the process of simulation
        for i in range(HOST_NUMBERS):
            env.process(self.total_hosts[i].packets_arrival(self.env))

    def simulating_process(self, env):
        global SLOT_NUMBER
        while True:
            #precisely finds out which queue will go through which slot
            slot_counter = 0
            slot_index = []
            for a in range(HOST_NUMBERS):
                if self.total_hosts[a].next_slot == SLOT_NUMBER:
                    counter += 1
                    slot_index.append(a)

            #When multiple queues want to transmit, this is handle collisions by Back_off Algo. kicking in
            if counter > 1:
                self.collisions += 1
                for i in slot_index:
                    self.total_hosts[a].collision_backoff()
            elif counter == 1:
                self.total_hosts[slot_index[0]].send_packet()
                self.packets_processed += 1

            yield env.timeout(self.slot_timing)
            SLOT_NUMBER += 1 # moving down to next slot

class host_simulation:
    def __init__(self,env,arrival_rate, expo_linear):
        self.env = env
        self.queue_len = 0
        self.arrival_rate = arrival_rate
        self.expo_linear = expo_linear
        self.targetted_slot = 0
        self.num_failures = 0

    def number_of_packets(self, env):
        #packets arrival
        while True:
            # Loop which is going to generate packets infinitively
            yield env.timeout(random.expovariate(self.arrival_rate))

            if self.queue_len == 0:
                self.reset_target()
            self.queue_len += 1

    # when collision occurs, in the process of packets being processed
    def backoff_collisions(self):
        if self.expoOrLinear:
            self.targetted_slot += random.randint(0,2**min(self.num_failures, 10)) + 1
        else:
            self.targetted_slot += random.randint(0,min(self.num_failures, 1024)) + 1

        self.num_failures += 1

    # rearranges the queue and get next packet ready
    def packet_in_queue(self):
        self.queue_len -= 1
        if self.queue_len > 0: # update the slot target and failures for the next packet
            self.reset_target()

    def target_rearranged(self):
        global SLOT_NUMBER
        self.slot_target = SLOT_NUMBER + 1 # target the next slot initially
        self.num_failures = 0 # reset failures/collisions to 0




def main():
    global SLOT_NUMBER
    print("Unsequenced Packet Simulation")
    for expo_linear in [True, False]:
        SimPlot.clf() # It will clear up the Plot
        if expo_linear:
            print("Exponential Backoff Algorithm")
        else:
            print("Linear Backoff Algorithm")

        print("{0:<20} {1:<12} {2:<20} {3:<15} {4:<10}".format(
        "Lambda", "Number of Slots", "Throughput" , "Processed Packets" , "Collisions"))

        x = []
        y = []

        for arrival_rate in [0.01, 0.02, 0.03, 0.04, 0.05 , 0.06 , 0.07 , 0.08 , 0.09]:
            SLOT_NUMBER = 0
            env = simpy.Environment()
            host_sim = [host_simulation(env,arrival_rate, expo_linear) for i in range(HOST_NUMBERS)]
            Ethernet = Ethernet_Simulation(env, SLOT_PER_RATE, host_sim)
            env.process(Ethernet.simulating_process(env))
            env.run(until=SIM_TIME)

            Throughput = float(Ethernet.packets_processed) / SLOT_NUMBER, 5
            x.append(arrival_rate)
            y.append(Throughput)

            print("{0:<9.3f} {1:<12.5f} {2:<9} {3:<9} {4:<9}".format(
                round(arrival_rate,3),
                SLOT_NUMBER,
                round(Throughput),
                ethernet.packets_processed,
                Ethernet.collisions
            ))

        SimPlot.axis([0, 0.1, 0, 1])
        SimPlot.xticks([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09])
        SimPlot.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        SimPlot.xlabel('Lambda')
        SimPlot.ylabel('Throughput')
        SimPlot.Plot(x,y, color='blue', marker='o')

        for i in range(9):
            SimPlot.annotate(s = str(y[i]), xy = (x[i], y[i]), xycoords='data', rotation=90, textcoords='offset points', xytext=(-5, 50))

        if exponential:
            SimPlot.title('Exponential Backoff: Lambda vs Throughput')
            SimPlot.savefig('exponential.png')
        else:
            SimPlot.title('Linear Backoff: Lambda vs Throughput')
            SimPlot.savefig('linear.png')



if __name__ == '__main__': main()

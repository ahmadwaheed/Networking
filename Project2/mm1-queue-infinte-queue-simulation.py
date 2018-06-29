   # This is a simpy based  simulation of a M/M/1 queue system
"""
"""
import random
import simpy
import math

RANDOM_SEED = None
SIM_TIME = 1000000
MU = 1



""" Queue system  """
class server_queue:
	def __init__(self, env, size_of_buffer, arrival_rate, Packet_Delay, Server_Idle_Periods):
		self.server = simpy.Resource(env, capacity = 1)
		self.env = env
		self.queue_len = 0
		self.flag_processing = 0
		self.packet_number = 0
		self.sum_time_length = 0
		self.start_idle_time = 0
		self.capacity_of_queue = size_of_buffer
		self.arrival_rate = arrival_rate
		self.Packet_Delay = Packet_Delay
		self.Server_Idle_Periods = Server_Idle_Periods

	def process_packet(self, env, packet):
		with self.server.request() as req:
			start = env.now
			yield req
			yield env.timeout(random.expovariate(MU))
			latency = env.now - packet.arrival_time
			self.Packet_Delay.addNumber(latency)
			#print("Packet number {0} with arrival time {1} latency {2}".format(packet.identifier, packet.arrival_time, latency))
			self.queue_len -= 1
			if self.queue_len == 0:
				self.flag_processing = 0
				self.start_idle_time = env.now

	def packets_arrival(self, env):
		# packet arrivals

		while True:
		     # Infinite loop for generating packets
			yield env.timeout(random.expovariate(self.arrival_rate))
			  # arrival time of one packet

			self.packet_number += 1
			  # packet id
			arrival_time = env.now
			#print(self.num_pkt_total, "packet arrival")
			#check if queue is smaller than capacity and if it is true, it will generate new packet
			if self.queue_len < self.capacity_of_queue:
				new_packet = Packet(self.packet_number,arrival_time)
				if self.flag_processing == 0:
					self.flag_processing = 1
					idle_period = env.now - self.start_idle_time
					self.Server_Idle_Periods.addNumber(idle_period)
				#print("Idle period of length {0} ended".format(idle_period))
				self.queue_len += 1
				env.process(self.process_packet(env, new_packet))


""" Packet class """
class Packet:
	def __init__(self, identifier, arrival_time):
		self.identifier = identifier
		self.arrival_time = arrival_time


class StatObject:
	def __init__(self):
		self.dataset =[]
		self.dropped_packets = 0
	def addNumber(self,x):
		self.dataset.append(x)
	def sum(self):
		n = len(self.dataset)
		sum = 0
		for i in self.dataset:
			sum = sum + i
		return sum
	def mean(self):
		n = len(self.dataset)
		sum = 0
		for i in self.dataset:
			sum = sum + i
		return sum/n
	def maximum(self):
		return max(self.dataset)
	def minimum(self):
		return min(self.dataset)
	def count(self):
		return len(self.dataset)
	def median(self):
		self.dataset.sort()
		n = len(self.dataset)
		if n//2 != 0: # get the middle number
			return self.dataset[n//2]
		else: # find the average of the middle two numbers
			return ((self.dataset[n//2] + self.dataset[n//2 + 1])/2)
	def standarddeviation(self):
		temp = self.mean()
		sum = 0
		for i in self.dataset:
			sum = sum + (i - temp)**2
		sum = sum/(len(self.dataset) - 1)
		return math.sqrt(sum)
	def addingDroppedPacket(self): #will add dropeed packets for probability
		self.dropped_packets += 1
	def totalAfterAddingDropped(self): #total number of packets generated.
		return len(self.dataset) + self.dropped_packets
	def packetLossProbability(self): #Actual probability of packet loss based on dropped packets/total packets
		return float(self.dropped_packets) / self.totalAfterAddingDropped()

#expected probability of packet loss
def lossProbabilityExpected(arrival_rate, size_of_buffer):
	return 1 - (float(math.pow(arrival_rate,size_of_buffer+1)-1)/(math.pow(arrival_rate, size_of_buffer+2)-1))

def main():
	print("Simple queue system model:mu = {0}".format(MU))
	print ("{0:<12} {1:<12} {2:<12} {3:<12} {4:<15} {5:<15} {6:<13} {7:<13} {8:<10}".format(
        "BufferSize", "Lambda", "TotalPkts", "ProcessedPkts", "DroppedPktsSimulation", "ExpectedDroppedPkts", "SimulatedProb", "ExpectedProb", "Mean"))
	random.seed(RANDOM_SEED)
	for Buffer in [10,50]:
		for arrival_rate in [0.2, 0.4, 0.6,  0.8, 0.9, 0.99]:
			env = simpy.Environment()
			Packet_Delay = StatObject()
			Server_Idle_Periods = StatObject()
			expected_dropped_packets = lossProbabilityExpected(arrival_rate, Buffer) * Packet_Delay.totalAfterAddingDropped()
			router = server_queue(env, arrival_rate, Buffer, Packet_Delay, Server_Idle_Periods)
			env.process(router.packets_arrival(env))
			env.run(until=SIM_TIME)
			print ("{0:<12} {1:<12f} {2:<12} {3:<13} {4:<21} {5:<19} {6:<14f} {7:<12f} {8:<12}".format(
				Buffer,
				round(arrival_rate, 3),
				int(Packet_Delay.totalAfterAddingDropped()),
				int(Packet_Delay.count()),
				int(Packet_Delay.dropped_packets),
				int(expected_dropped_packets),
				round(Packet_Delay.packetLossProbability(),8),
				round(lossProbabilityExpected(arrival_rate,Buffer),8),
				round(Packet_Delay.mean(), 3)
				))

if __name__ == '__main__': main()

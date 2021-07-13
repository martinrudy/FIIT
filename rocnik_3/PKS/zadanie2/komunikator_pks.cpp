#include <stdlib.h>
#include <string>
#include <WinSock2.h>
#include <Ws2tcpip.h>
#include <thread>
#include <iostream>
#include <stdint.h>
#include <thread>
#pragma comment(lib,"ws2_32.lib") 

#define BUFLEN 512	
#define PORT 8888	
#define MAX_FRAGMENT 1500
#define HEADER_SIZE 48


int keep_recieve = 0;
int pripojenie = 1;
int sprava = 3;
int chyba = 0;


struct custom_header {
	uint16_t massage_type;
	uint32_t fragment_number;
	uint32_t fragment_size;
	uint32_t fragment_sum;
	uint32_t header_checksum;
};


unsigned short getCRC(const unsigned char* data_p, unsigned char length) {
	unsigned char x;
	unsigned short crc = 0xFFFF;

	while (length--) {
		x = crc >> 8 ^ *data_p++;
		x ^= x >> 4;
		crc = (crc << 8) ^ ((unsigned short)(x << 12)) ^ ((unsigned short)(x << 5)) ^ ((unsigned short)x);
	}
	return crc;
}



void keep_alive(struct sockaddr_in destAddress, SOCKET s) {
	struct custom_header header;
	header.massage_type = 22;
	header.header_checksum = 0;
	header.fragment_number = 0;
	header.fragment_size = 0;
	header.fragment_number = 0;

	int keep_sent = 0;
	clock_t start = clock();


	while (1) {
		clock_t end = clock();
		float seconds = (float)(end - start) / CLOCKS_PER_SEC;
		if (keep_sent - keep_recieve >= 3) {
			pripojenie = 0;
			break;
		}
		if (seconds >= 45) {
			if (sendto(s, (char*)&header, sizeof(header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
			{
				printf("sendto() failed with error code : %d", WSAGetLastError());
				exit(EXIT_FAILURE);
			}
			else {
				keep_sent++;
				printf("keep alive sent");
			}
		}
	}
}

void server(int port) {
	WSADATA wsa;
	SOCKET sockfd;
	struct sockaddr_in serverAddr, newAddr;
	char buffer[1024];
	socklen_t addr_size;

	int offset = 0;
	int frame_id = 0;
	custom_header* packet_recv;
	custom_header packet_send;
	uint32_t CRC = 0;

	char inicializacia[sizeof(struct custom_header)];

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		printf("Failed. Error Code : %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	sockfd = socket(AF_INET, SOCK_DGRAM, 0);

	memset(&serverAddr, '\0', sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(port);
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	//serverAddr.sin_addr.s_addr = inet_addr("192.168.0.109");

	bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
	addr_size = sizeof(newAddr);

	while (1) {
		if (sprava == 0) {
			int f_recv_size = recvfrom(sockfd, inicializacia, sizeof(struct custom_header), 0, (struct sockaddr*)&newAddr, &addr_size);
			packet_recv = (struct custom_header*)inicializacia;
			if (f_recv_size > 0 && (packet_recv->massage_type == 0 || packet_recv->massage_type == 2)) {
				printf("[+]Frame Received: size: %d  number: %d\n", packet_recv->fragment_size + HEADER_SIZE, packet_recv->fragment_number);


				int fragment = packet_recv->fragment_size;
				char* data_fragment = (char*)malloc((fragment + sizeof(struct custom_header)) * sizeof(char));
				int poc = 0;
				char* message = (char*)malloc((packet_recv->fragment_number + 1) * sizeof(char));
				int fragment_sum = packet_recv->fragment_sum;
				int velkost_suboru = packet_recv->fragment_number;

				packet_send.fragment_sum = 0;
				packet_send.massage_type = 1;
				packet_send.fragment_number = frame_id + 1;

				sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
				printf("[+]Ack Send\n");




				while (packet_recv->massage_type != 2) {
					int f_recv_size = recvfrom(sockfd, data_fragment, fragment + sizeof(struct custom_header), 0, (struct sockaddr*)&newAddr, &addr_size);
					packet_recv = (struct custom_header*)data_fragment;

					if (fragment + packet_recv->fragment_sum > velkost_suboru) {
						offset = velkost_suboru - packet_recv->fragment_sum;
						poc = packet_recv->fragment_sum - offset;
					}
					else {
						offset = fragment;
						poc = offset;
					}

					CRC = packet_recv->header_checksum;
					packet_recv->header_checksum = 0;
					if (getCRC((unsigned char*)data_fragment, poc + sizeof(struct custom_header)) != CRC) {
						packet_send.fragment_sum = 0;
						packet_send.massage_type = 8;
						packet_send.fragment_number = packet_recv->fragment_number + 1;

						printf("zly checksum\n");
						sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
						printf("[+]Ack Send\n");
					
					}
					else {
						if (f_recv_size > 0 && packet_recv->massage_type == 1 && packet_recv->fragment_number == frame_id) {
							printf("[+]Frame Received: size: %d  number: %d\n", packet_recv->fragment_size + HEADER_SIZE, packet_recv->fragment_number);
						}
						else {
							printf("[+]Frame Not Received\n");
						}

						for (int x = 0; x < offset; x++) {
							message[packet_recv->fragment_sum + x] = data_fragment[x + sizeof(struct custom_header)];
						}

						packet_send.fragment_sum = 0;
						packet_send.massage_type = 1;
						packet_send.fragment_number = packet_recv->fragment_number + 1;

						sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
						printf("[+]Ack Send\n");

						frame_id++;
					}
				
				}
				FILE* subor;

				subor = fopen("mam.txt", "wb+");

				_fullpath(buffer, "mam.txt", _MAX_PATH);
				fwrite(message, 1, velkost_suboru, subor);
				printf("subor prijaty %s\n", buffer);
				fclose(subor);
			}
			else {
				printf("[+]Frame Not Received\n");
				sprava = 3;
			}
		}
		if (sprava == 3) {
			int f_recv_size = recvfrom(sockfd, inicializacia, sizeof(struct custom_header), 0, (struct sockaddr*)&newAddr, &addr_size);
			packet_recv = (struct custom_header*)inicializacia;
			if (f_recv_size > 0 && (packet_recv->massage_type == 0 || packet_recv->massage_type == 2)) {
				printf("[+]Frame Received: size: %d  number: %d\n", packet_recv->fragment_size + HEADER_SIZE, packet_recv->fragment_number);


				int fragment = packet_recv->fragment_size;
				char* data_fragment = (char*)malloc((fragment + sizeof(struct custom_header)) * sizeof(char));
				int poc = 0;
				char* message = (char*)malloc((packet_recv->fragment_number + 1) * sizeof(char));
				int fragment_sum = packet_recv->fragment_sum;
				int velkost_suboru = packet_recv->fragment_number;

				packet_send.fragment_sum = 0;
				packet_send.massage_type = 1;
				packet_send.fragment_number = frame_id + 1;

				sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
				printf("[+]Ack Send\n");




				while (packet_recv->massage_type != 2) {
					int f_recv_size = recvfrom(sockfd, data_fragment, fragment + sizeof(struct custom_header), 0, (struct sockaddr*)&newAddr, &addr_size);
					packet_recv = (struct custom_header*)data_fragment;

					if (fragment + packet_recv->fragment_sum > velkost_suboru) {
						offset = velkost_suboru - packet_recv->fragment_sum;
						poc = packet_recv->fragment_sum - offset;
					}
					else {
						offset = fragment;
						poc = offset;
					}

					CRC = packet_recv->header_checksum;
					packet_recv->header_checksum = 0;
					if (getCRC((unsigned char*)data_fragment, poc + sizeof(struct custom_header)) != CRC) {
						printf("zly checksum\n");
					}

					if (f_recv_size > 0 && packet_recv->massage_type == 1 && packet_recv->fragment_number == frame_id) {
						printf("[+]Frame Received: size: %d  number: %d\n", packet_recv->fragment_size + HEADER_SIZE, packet_recv->fragment_number);
					}
					else {
						printf("[+]Frame Not Received\n");
					}

					for (int x = 0; x < offset; x++) {
						message[packet_recv->fragment_sum + x] = data_fragment[x + sizeof(struct custom_header)];
					}

					packet_send.fragment_sum = 0;
					packet_send.massage_type = 1;
					packet_send.fragment_number = packet_recv->fragment_number + 1;

					sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
					printf("[+]Ack Send\n");

					frame_id++;
				}
				FILE* subor;

				subor = fopen("mam.txt", "wb+");

				_fullpath(buffer, "mam.txt", _MAX_PATH);
				fwrite(message, 1, velkost_suboru, subor);
				printf("subor prijaty %s\n", buffer);
				fclose(subor);
			}
			else {
				printf("[+]Frame Not Received\n");
				sprava = 3;
			}
		}
		else if (sprava == 1) {
			int f_recv_size = recvfrom(sockfd, inicializacia, sizeof(struct custom_header), 0, (struct sockaddr*)&newAddr, &addr_size);
			packet_recv = (struct custom_header*)inicializacia;
			if (f_recv_size > 0 && packet_recv->massage_type == 0) {
				printf("[+]Frame Received: size: %d  number: %d\n", packet_recv->fragment_size + HEADER_SIZE, packet_recv->fragment_number);


				int fragment = packet_recv->fragment_size;
				char* data_fragment = (char*)malloc((fragment + sizeof(struct custom_header)) * sizeof(char));

				char* message = (char*)malloc((packet_recv->fragment_number + 1) * sizeof(char));
				int fragment_sum = packet_recv->fragment_sum;
				int velkost_suboru = packet_recv->fragment_number;

				packet_send.fragment_sum = 0;
				packet_send.massage_type = 1;
				packet_send.fragment_number = frame_id + 1;

				sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
				printf("[+]Ack Send\n");




				while (packet_recv->massage_type != 2) {
					int f_recv_size = recvfrom(sockfd, data_fragment, fragment + sizeof(struct custom_header), 0, (struct sockaddr*)&newAddr, &addr_size);
					packet_recv = (struct custom_header*)data_fragment;

					if (fragment + packet_recv->fragment_sum > velkost_suboru) {
						offset = velkost_suboru - packet_recv->fragment_sum;
					}
					else {
						offset = fragment;
					}

					CRC = packet_recv->header_checksum;
					packet_recv->header_checksum = 0;
					if (getCRC((unsigned char*)data_fragment, offset + sizeof(struct custom_header)) != CRC) {
						printf("zly chechsum\n");
					}

					if (f_recv_size > 0 && packet_recv->massage_type == 1 && packet_recv->fragment_number == frame_id) {
						printf("[+]Frame Received: size: %d  number: %d\n", packet_recv->fragment_size + HEADER_SIZE, packet_recv->fragment_number);
					}
					else {
						printf("[+]Frame Not Received\n");
					}

					for (int x = 0; x < offset; x++) {
						message[packet_recv->fragment_sum + x] = data_fragment[x + sizeof(struct custom_header)];
					}

					packet_send.fragment_sum = 0;
					packet_send.massage_type = 1;
					packet_send.fragment_number = packet_recv->fragment_number + 1;

					sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
					printf("[+]Ack Send\n");

					frame_id++;
				}
				printf("%s", message);
			}

			if (f_recv_size > 0 && packet_recv->massage_type == 22) {
				packet_send.fragment_sum = 0;
				packet_send.massage_type = 22;
				packet_send.fragment_number = 0;
				packet_send.fragment_size = 0;
				packet_send.header_checksum = 0;

				sendto(sockfd, (char*)&packet_send, sizeof(packet_send), 0, (struct sockaddr*)&newAddr, addr_size);
				printf("keep alive replied\n");
			}
			else {
				printf("[+]Frame Not Received\n");
			}
		}


	}

	closesocket(sockfd);
	WSACleanup();
}

void client() {
	SOCKET s;
	struct sockaddr_in destAddress, si_other;
	int slen, recv_len;
	char buf[BUFLEN];
	WSADATA wsa;
	custom_header *packet_send;
	custom_header packet_recv;

	int frame_id = 0;
	int ack_recv = 1;
	int port;

	char ip_adress[15];
	int offset = 0;
	int fragment = 0;
	char file_name[101];
	char* message;
	long message_len, file_len;
	unsigned int fragment_sum = 0;
	int message_len_actual = 0;
	int choice = 0;

	char inicializacia[sizeof(struct custom_header)];


	//Initialise winsock
	printf("\nInitialising Winsock...");
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		printf("Failed. Error Code : %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}
	printf("Initialised.\n");

	//Create a socket
	if ((s = socket(AF_INET, SOCK_DGRAM, 0)) == INVALID_SOCKET)
	{
		printf("Could not create socket : %d", WSAGetLastError());
	}
	printf("Socket created.\n");


	printf("zadaj port: ");
	scanf("%d", &port);
	printf("zadaj ip adressu: ");
	scanf("%s", ip_adress);

	memset(&destAddress, '\0', sizeof(destAddress));
	destAddress.sin_family = AF_INET;
	destAddress.sin_addr.s_addr = INADDR_ANY;
	destAddress.sin_port = htons(port);
	inet_pton(AF_INET, ip_adress, &destAddress.sin_addr.s_addr);

	std::thread thread_obj(server, port);

	while (1) {
		printf("1 -poslat spravu\n");
		printf("2 -poslat subor\n");
		printf("3 -poslat chybny\n");
		scanf("%d", &choice);


		printf("zadaje velkost fragmentu: ");
		scanf("%d", &fragment);


		if ((s = socket(AF_INET, SOCK_DGRAM, 0)) == INVALID_SOCKET)
		{
			printf("Could not create socket : %d", WSAGetLastError());
		}
		printf("Socket created.\n");

		if (choice == 1) {
			sprava = 1;
			printf("zadaj spravu:");
			scanf("%s", buf);

			unsigned char* ukazovatel_na_data;
			char* data_fragment = (char*)malloc(fragment + sizeof(custom_header));
			message_len = strlen(buf);


			while (fragment < HEADER_SIZE || fragment > MAX_FRAGMENT) {
				printf("Zadali ste neplatnu velkost.\nVelkost musi byt z rozsahu %d - %d\nZadajte velkost fragmentu: ", HEADER_SIZE + 1, MAX_FRAGMENT);
				scanf("%d", &fragment);
			}
			fragment -= HEADER_SIZE;

			if (message_len > fragment) {
				fragment_sum = strlen(buf) / (int)fragment + 1;
			}
			else {
				fragment_sum = 1;
			}

			packet_send = (struct custom_header*)inicializacia;

			packet_send->massage_type = 0;
			packet_send->fragment_sum = fragment_sum;
			packet_send->fragment_size = fragment;
			packet_send->header_checksum = 0;
			packet_send->fragment_number = strlen(buf);

			packet_send = (struct custom_header*)inicializacia;


			if (sendto(s, inicializacia, sizeof(struct custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
			{
				printf("sendto() failed with error code : %d", WSAGetLastError());
				exit(EXIT_FAILURE);
			}
			else {
				printf("[+]Init send  size %d \n", sizeof(struct custom_header));
			}

			int addr_size = sizeof(destAddress);
			int f_recv_size = recvfrom(s, (char*)&packet_recv, sizeof(packet_recv), 0, (struct sockaddr*)&destAddress, &addr_size);
			if (f_recv_size > 0 && packet_recv.fragment_sum == 0 && packet_recv.fragment_number == frame_id + 1) {
				printf("[+]Connected\n");
				//std::thread thread_obj(keep_alive, destAddress, s);
				ack_recv = 1;
			}
			else {
				printf("[-]Ack Not Received\n");
				ack_recv = 0;
			}
			offset = fragment;
			while (1) {
				int i = 0;
				int temp = offset - fragment;
				packet_send = (struct custom_header*)data_fragment;
				packet_send->massage_type = 1;
				packet_send->fragment_sum = temp;
				packet_send->fragment_size = fragment;
				packet_send->header_checksum = 0;
				packet_send->fragment_number = frame_id;
				ukazovatel_na_data = (unsigned char*)data_fragment;

				if (offset < message_len) {
					for (temp; temp < offset; temp++) {
						data_fragment[sizeof(struct custom_header) + i] = buf[temp];
						i++;
					}
				}
				else if (offset > message_len) {
					offset -= (offset - message_len);
					for (temp; temp < offset; temp++) {
						data_fragment[sizeof(struct custom_header) + i++] = buf[temp];
					}
				}
				else {
					for (temp; temp < offset; temp++) {
						data_fragment[sizeof(struct custom_header) + i++] = buf[temp];
					}
				}


				if (ack_recv == 1) {

					packet_send->massage_type = 1;
					packet_send->fragment_number = frame_id;
					packet_send->header_checksum = getCRC((unsigned char*)data_fragment, offset + sizeof(struct custom_header));
					printf("%s", packet_send->header_checksum);


					if (sendto(s, data_fragment, fragment + sizeof(custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
					{
						printf("sendto() failed with error code : %d", WSAGetLastError());
						exit(EXIT_FAILURE);
					}
					printf("[+]Frame Send size %d frame number %d\n", packet_send->fragment_size + HEADER_SIZE, packet_send->fragment_number);
				}
				int addr_size = sizeof(destAddress);
				int f_recv_size = recvfrom(s, (char*)&packet_recv, sizeof(packet_recv), 0, (struct sockaddr*)&destAddress, &addr_size);

				if (f_recv_size > 0 && packet_recv.fragment_sum == 0 && packet_recv.fragment_number == frame_id + 1) {
					printf("[+]Ack Received\n");
					ack_recv = 1;
				}
				else {
					printf("[-]Ack Not Received\n");
					ack_recv = 0;
				}
				if (offset == message_len) {
					packet_send->massage_type = 2;
					if (sendto(s, data_fragment, fragment + sizeof(custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
					{
						printf("sendto() failed with error code : %d", WSAGetLastError());
						exit(EXIT_FAILURE);
					}
					break;
				}
				frame_id++;
				offset += fragment;
			}


		}

		else if (choice == 2 || choice == 3) {
			if (choice == 3) {
				chyba = 1;
			}
			else {
				chyba = 0;
			}
			sprava = 0;
			printf("zadaj cestu k suboru: ");
			scanf("%s", file_name);



			while (fragment < HEADER_SIZE || fragment > MAX_FRAGMENT) {
				printf("Zadali ste neplatnu velkost.\nVelkost musi byt z rozsahu %d - %d\nZadajte velkost fragmentu: ", HEADER_SIZE + 1, MAX_FRAGMENT);
				scanf("%d", &fragment);
			}
			fragment -= HEADER_SIZE;

			unsigned char* ukazovatel_na_data;
			char* data_fragment = (char*)malloc(fragment + sizeof(custom_header));

			FILE* file;

			if ((file = fopen(file_name, "rb+")) == NULL) {
				printf("No file name!\n");
				break;
			}

			fseek(file, 0, SEEK_END);
			file_len = ftell(file);
			rewind(file);
			message = (char*)malloc(file_len * sizeof(char));
			fread(message, 1, file_len, file);
			message_len = file_len;
			fclose(file);


			if (message_len > fragment) {
				fragment_sum = (int)message_len / (int)fragment + 1;
			}
			else {
				fragment_sum = 1;
			}

			packet_send = (struct custom_header*)inicializacia;

			packet_send->massage_type = 0;
			packet_send->fragment_sum = fragment_sum;
			packet_send->fragment_size = fragment;
			packet_send->header_checksum = 0;
			packet_send->fragment_number = message_len;

			if (sendto(s, inicializacia, sizeof(struct custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
			{
				printf("sendto() failed with error code : %d", WSAGetLastError());
				exit(EXIT_FAILURE);
			}
			else {
				printf("[+]Init send  size %d \n", sizeof(struct custom_header));
			}

			int addr_size = sizeof(destAddress);
			int f_recv_size = recvfrom(s, (char*)&packet_recv, sizeof(packet_recv), 0, (struct sockaddr*)&destAddress, &addr_size);

			if (f_recv_size > 0 && (packet_recv.massage_type == 0 || packet_recv.massage_type == 1)) {
				printf("[+]Connected\n");
				//std::thread thread_obj(keep_alive, destAddress, s);
				ack_recv = 1;
			}
			//keepalive
			else if (f_recv_size > 0 && packet_recv.massage_type == 22) {
				keep_recieve++;
			}
			else {
				printf("[-]Ack Not Received\n");
				ack_recv = 0;
			}

			offset = fragment;
			while (1) {
				int i = 0;
				int temp = offset - fragment;
				packet_send = (struct custom_header*)data_fragment;
				packet_send->massage_type = 1;
				packet_send->fragment_sum = temp;
				packet_send->fragment_size = fragment;
				packet_send->header_checksum = 0;
				packet_send->fragment_number = frame_id;
				ukazovatel_na_data = (unsigned char*)data_fragment;

				if (offset < message_len) {
					for (temp; temp < offset; temp++) {
						data_fragment[sizeof(struct custom_header) + i] = message[temp];
						i++;
					}
				}
				else if (offset > message_len) {
					fragment = offset - message_len;
					offset -= (offset - message_len);

					for (temp; temp < offset; temp++) {
						data_fragment[sizeof(struct custom_header) + i++] = message[temp];
					}
				}
				else {
					for (temp; temp < offset; temp++) {
						data_fragment[sizeof(struct custom_header) + i++] = message[temp];
					}
				}


				if (ack_recv == 1) {

					if (chyba == 1) {
						packet_send->massage_type = 1;
						packet_send->fragment_number = frame_id;
						packet_send->header_checksum = 0;

						packet_send->header_checksum = getCRC((unsigned char*)data_fragment, fragment + sizeof(struct custom_header)) + 20;

						if (sendto(s, data_fragment, fragment + sizeof(custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
						{
							printf("sendto() failed with error code : %d", WSAGetLastError());
							exit(EXIT_FAILURE);
						}
						printf("[+]Frame Send size %d frame number %d\n", packet_send->fragment_size + HEADER_SIZE, packet_send->fragment_number);
					}
					else {
						packet_send->massage_type = 1;
						packet_send->fragment_number = frame_id;
						packet_send->header_checksum = 0;

						printf("%d", fragment);
						packet_send->header_checksum = getCRC((unsigned char*)data_fragment, fragment + sizeof(struct custom_header));

						if (sendto(s, data_fragment, fragment + sizeof(custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
						{
							printf("sendto() failed with error code : %d", WSAGetLastError());
							exit(EXIT_FAILURE);
						}
						printf("[+]Frame Send size %d frame number %d\n", packet_send->fragment_size + HEADER_SIZE, packet_send->fragment_number);
					}

				}
				int addr_size = sizeof(destAddress);
				int f_recv_size = recvfrom(s, (char*)&packet_recv, sizeof(packet_recv), 0, (struct sockaddr*)&destAddress, &addr_size);

				if (f_recv_size > 0 && packet_recv.fragment_sum == 0 && packet_recv.fragment_number == frame_id + 1) {
					printf("[+]Ack Received\n");
					ack_recv = 1;
				}
				else {
					printf("[-]Ack Not Received\n");
					ack_recv = 0;
				}
				if (packet_recv.massage_type == 8) {
					packet_send->massage_type = 1;
					packet_send->fragment_number = frame_id;
					packet_send->header_checksum = 0;

					printf("%d", fragment);
					packet_send->header_checksum = getCRC((unsigned char*)data_fragment, fragment + sizeof(struct custom_header));

					if (sendto(s, data_fragment, fragment + sizeof(custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
					{
						printf("sendto() failed with error code : %d", WSAGetLastError());
						exit(EXIT_FAILURE);
					}
					printf("[+]Frame Send size %d frame number %d\n", packet_send->fragment_size + HEADER_SIZE, packet_send->fragment_number);
				}
				if (offset == message_len) {
					packet_send->massage_type = 2;
					packet_send->fragment_number = frame_id;
					packet_send->header_checksum = 0;


					packet_send->header_checksum = getCRC((unsigned char*)data_fragment, fragment + sizeof(struct custom_header));
					if (sendto(s, data_fragment, fragment + sizeof(custom_header), 0, (struct sockaddr*)&destAddress, sizeof(destAddress)) == SOCKET_ERROR)
					{
						printf("sendto() failed with error code : %d", WSAGetLastError());
						exit(EXIT_FAILURE);
					}
					break;
				}
				frame_id++;
				offset += fragment;
			}

		}
		closesocket(s);

	}
	
	WSACleanup();
}

int main() {
	while (1) {
		int port;
		int menu = 0;
		printf("Vyber funkciu:\n");
		printf("1 -Server\n");
		printf("2 -Klient\n");
		printf("0 -Koniec aplikacie\n");
		printf("Zadajte cislo vasej volby: ");
		scanf("%d", &menu);
		if (menu == 1) {
			printf("zadaj port: ");
			scanf("%d", &port);
			server(port);
		}
		else if (menu == 2) {
			client();
		}
	}
	

	return 0;
}
#include <stdlib.h>
#include <stdio.h>
 
#include <pcap.h>
 
#define LINE_LEN 16

struct sniff_ethernet {
	u_char ether_dhost[6]; 
	u_char ether_shost[6]; 
	u_short ether_type; 
};

struct ieee {
	u_short prve_2;
};

void print_len(int packet_number, int i, int x) {
	FILE* f = fopen("vypis.txt", "a");

	fprintf(f, "Ramec %i\n", packet_number);
	fprintf(f, "Dlzka ramca poskytnuta pcap API %d B\n", i);
	printf("Ramec %i\n", packet_number);						
	printf("Dlzka ramca poskytnuta pcap API %d B\n", i);   
	x = x + 4;
	if (x < 64)x = 64;
	printf("Dlzka ramca prenasaneho po mediu %d B\n", x);
	fprintf(f, "Dlzka ramca prenasaneho po mediu %d B\n", x);

	fclose(f);
}
 
u_short convert(u_short x) {
	return x = (x >> 8) | ((x & 255) << 8);
}

void find_ethertype(u_short ether_type, u_short prve_2) {
	FILE* hodnoty = fopen("hodnoty.txt", "r");
	FILE* f = fopen("vypis.txt", "a");
	int i = 0;
	char c;
	
	if (ether_type >= 1500) {
		fprintf(f, "Ethernet II\n");
		printf("Ethernet II\n");
	}
	else {
		while(1){
			fscanf(hodnoty, "%d", &i);
			if (i == prve_2) {
				while ((c = getc(hodnoty)) != '\n') {
					printf("%c", c);
					fprintf(f, "c", c);
				}
				printf("\n");
				break;
			}
			else if (i == 0) {
				while ((c = getc(hodnoty)) != '\n') {
					printf("%c", c);
					fprintf(f, "c", c);
				}
				printf("\n");
				break;
			}
			else {
				while ((c = getc(hodnoty)) != '\n');
			}
		}
	}
	fclose(hodnoty);
	fclose(f);

}

void print_mac(u_char *dhost, u_char *shost) {
	FILE* f;
	f = fopen("vypis.txt", "a");
	fprintf(f, "Destination MAC Address : %02x:%02x:%02x:%02x:%02x:%02x\n", dhost[0], dhost[1], dhost[2], dhost[3], dhost[4], dhost[5]);
	fprintf(f, "Source MAC Address : %02x:%02x:%02x:%02x:%02x:%02x\n", shost[0], shost[1], shost[2], shost[3], shost[4], shost[5]);

	printf("Destination MAC Address : %02x:%02x:%02x:%02x:%02x:%02x\n", dhost[0], dhost[1], dhost[2], dhost[3], dhost[4], dhost[5]);
	printf("Source MAC Address : %02x:%02x:%02x:%02x:%02x:%02x\n", shost[0], shost[1], shost[2], shost[3], shost[4], shost[5]);
	fclose(f);
}

int main()
{
	while (1) {
		int prepinac = 0;

		printf("Zadaj 1 pre vypis ramcov\n");
		printf("Zadaj 2 pre ukoncenie programu\n");

		scanf("%d", &prepinac);

		if (prepinac == 1) {
			pcap_t* fp;
			char errbuf[PCAP_ERRBUF_SIZE];
			char source[PCAP_BUF_SIZE];
			struct pcap_pkthdr* header;
			const u_char* pkt_data;
			u_int i = 0;
			int res;
			int prepinac;
			char path[201];

			FILE* f = fopen("vypis.txt", "w");

			fprintf(f, " ");
			fclose(f);


			printf("vymaz vypis.txt\n");
			printf("zadaj cestu k suboru\n");
			scanf("%s", path);
			char* filename = path;



			/* Create the source string according to the new WinPcap syntax */
			if (pcap_createsrcstr(source,         // variable that will keep the source string
				PCAP_SRC_FILE,  // we want to open a file
				NULL,           // remote host
				NULL,           // port on the remote host
				filename,        // name of the file we want to open
				errbuf          // error buffer
			) != 0)
			{
				fprintf(stderr, "\nError creating a source string\n");
				return -1;
			}

			/* Open the capture file */
			if ((fp = pcap_open(source,         // name of the device
				65536,          // portion of the packet to capture
								// 65536 guarantees that the whole packet will be captured on all the link layers
				PCAP_OPENFLAG_PROMISCUOUS,     // promiscuous mode
				1000,              // read timeout
				NULL,              // authentication on the remote machine
				errbuf         // error buffer
			)) == NULL)
			{
				fprintf(stderr, "\nUnable to open the file %s.\n", source);
				return -1;
			}

			int packet_number = 0;

			/* Retrieve the packets from the file */
			while ((res = pcap_next_ex(fp, &header, &pkt_data)) >= 0)
			{
				FILE* f = fopen("vypis.txt", "a");

				printf("Packet number (%d)\n", ++packet_number);

				fprintf(f, "Packet number (%d)\n", packet_number);
				/* print pkt timestamp and pkt len */
				//printf("%ld:%ld (%ld)\n", header->ts.tv_sec, header->ts.tv_usec, header->len);
				//fprintf(f, "%ld:%ld (%ld)\n", header->ts.tv_sec, header->ts.tv_usec, header->len);

				print_len(packet_number, header->caplen, header->len);

				struct sniff_ethernet* ethernet = (struct ethernet*)(pkt_data);
				u_short ethernet_type = convert(ethernet->ether_type);

				struct ieee* ieee = (struct ieee*)(pkt_data);
				u_short prve_2 = convert(ieee->prve_2);


				find_ethertype(ethernet_type, prve_2);

				print_mac(ethernet->ether_dhost, ethernet->ether_shost);

				/*else if (ieee->prve_2 == 65535) {
					printf("IEEE 802.3 Novell Raw\n");
				}
				else if (ieee->prve_2 == 43690) {
					printf("IEEE 802.3 Snap\n");
				}
				else {
					printf("IEEE 802.3 LLC\n");
				}*/

				for (i = 1; (i < header->caplen + 1); i++)
				{
					printf("%.2x ", pkt_data[i - 1]);
					fprintf(f, "%.2x ", pkt_data[i - 1]);
					if ((i % LINE_LEN) == 0) {
						printf("\n");
						fprintf(f, "\n");
					}
				}

				printf("\n\n");
				fprintf(f, "\n\n");
				fclose(f);
			}

			if (res == -1)
			{
				printf("Error reading the packets: %s\n", pcap_geterr(fp));
			}
			
		}
		else if (prepinac == 2) {
			break;
		}
	}
	return 0;
}
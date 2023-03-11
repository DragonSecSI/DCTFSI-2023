// gcc server.c -o app -pthread

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>

#define PORT 10000
#define BUFFER_SIZE 256
#define MAX_THREADS 5

int num_threads;
int listener;

long buf;
char *filename;

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t buf_lock = PTHREAD_MUTEX_INITIALIZER;

int create_listener()
{
	int retval, listener;

	struct sockaddr_un conf;
	conf.sun_family = AF_UNIX;
	strcpy(conf.sun_path, filename);
	listener = socket(AF_UNIX, SOCK_STREAM, 0);
	if (listener == -1) {
		puts("Error creating socket");
		exit(1);
	}

	retval = bind(listener, (struct sockaddr *)&conf, sizeof(conf));
	if (retval == -1) {
		puts("Bind failed");
		close(listener);
		exit(1);
	}
	if (listen(listener, 5) == -1) {
		puts("Listen failed");
		close(listener);
		exit(1);
	}
	return listener;
}

int accept_conn()
{
	int client = accept(listener, NULL, NULL);
	if (client == -1) {
		puts("Accept failed");
		close(listener);
		exit(1);
	}
	printf("Accepted client: %d\n", client);
	return client;
}

int receive(int client)
{
	int retval = recv(client, &buf, 8, 0);
	if (retval < 0) {
		puts("Recv failed");
		close(client);
		return -1;
	} else if (retval == 0) {
		puts("Connection closing...");
		return 0;
	}
	//printf("read %d bytes\n", retval);
	return retval;
}

int send_back(int client, char *buf)
{
	int retval = send(client, buf, strlen(buf), 0);
	if (retval == -1) {
		puts("Send failed");
		close(client);
		return -1;
	}
	return retval;
}

int vuln(int client)
{
	int retval = 0;
	if (buf == 0x1337c0de) {
		retval = send_back(client, "You are in\n");
		int fd = open("flag.txt", O_RDONLY);
		char *flag = calloc(BUFFER_SIZE, sizeof(char));
		if (buf == 0xdeadc0de) {
			retval = read(fd, flag, BUFFER_SIZE - 1);
			retval = send_back(client, flag);
		} else {
			retval = send_back(client, "Nope!\n");
		}
		free(flag);
		close(fd);
	} else {
		retval = send_back(client, "Nope!\n");
	}
	return retval;
}

void *serve(void *arg)
{
	int retval;
	int client = accept_conn();

	do {
		retval = receive(client);
		if (retval > 0) {
			retval = vuln(client);
		}
	} while (retval > 0);

	close(client);
	pthread_mutex_lock(&lock);
	num_threads--;
	pthread_mutex_unlock(&lock);

	return NULL;
}

int main(int argc, char **argv)
{
	if (argc < 2) {
		printf("Usage: %s file.sock\n", argv[0]);
		return 1;
	}
	filename = argv[1];

	num_threads = 0;
	listener = create_listener();
	pthread_t thread;

	while (1) {
		if (num_threads < MAX_THREADS) {
			pthread_mutex_lock(&lock);
			num_threads++;
			pthread_mutex_unlock(&lock);
			pthread_create(&thread, NULL, serve, NULL);
			pthread_detach(thread);
		}
	}

	pthread_mutex_destroy(&lock);

	return 0;
}

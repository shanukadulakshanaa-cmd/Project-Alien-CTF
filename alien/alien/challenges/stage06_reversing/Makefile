CC = gcc
CFLAGS = -o
TARGET = doomsday.elf
SOURCE = doomsday.c

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(TARGET) $(SOURCE)

clean:
	rm -f $(TARGET)

.PHONY: all clean

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <PCSC/winscard.h>

int main() {
    SCARDCONTEXT hContext;
    SCARDHANDLE hCard;
    DWORD dwActiveProtocol;
    LONG rv;
    LPTSTR pmszReaders = NULL;
    DWORD dwReaders = SCARD_AUTOALLOCATE;

    // Establish context
    rv = SCardEstablishContext(SCARD_SCOPE_SYSTEM, NULL, NULL, &hContext);
    if (rv != SCARD_S_SUCCESS) {
        printf("Failed to establish context: %s\n", pcsc_stringify_error(rv));
        return 1;
    }

    // List readers
    rv = SCardListReaders(hContext, NULL, (LPTSTR)&pmszReaders, &dwReaders);
    if (rv != SCARD_S_SUCCESS) {
        printf("Failed to list readers: %s\n", pcsc_stringify_error(rv));
        SCardReleaseContext(hContext);
        return 1;
    }

    if (dwReaders <= 1) { // no readers or empty list
        printf("No PC/SC readers found.\n");
        SCardFreeMemory(hContext, pmszReaders);
        SCardReleaseContext(hContext);
        return 1;
    }

    char *reader = pmszReaders;
    printf("Using reader: %s\n", reader);

    // Connect to card
    rv = SCardConnect(hContext, reader, SCARD_SHARE_SHARED,
                     SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1, &hCard, &dwActiveProtocol);
    if (rv != SCARD_S_SUCCESS) {
        printf("Failed to connect to card: %s\n", pcsc_stringify_error(rv));
        SCardFreeMemory(hContext, pmszReaders);
        SCardReleaseContext(hContext);
        return 1;
    }

    printf("Card connected.\n");

    // APDU command to get UID for ACR122U
    BYTE cmdGetUID[] = { 0xFF, 0xCA, 0x00, 0x00, 0x00 };
    BYTE recvBuffer[256];
    DWORD recvLength = sizeof(recvBuffer);

    rv = SCardTransmit(hCard,
                       (dwActiveProtocol == SCARD_PROTOCOL_T0) ? SCARD_PCI_T0 : SCARD_PCI_T1,
                       cmdGetUID, sizeof(cmdGetUID), NULL, recvBuffer, &recvLength);
    if (rv != SCARD_S_SUCCESS) {
        printf("Failed to transmit: %s\n", pcsc_stringify_error(rv));
    } else {
        printf("Card UID: ");
        for (DWORD i = 0; i < recvLength - 2; i++) { // Last two bytes are status words SW1 SW2
            printf("%02X ", recvBuffer[i]);
        }
        printf("\n");
    }

    // Clean up
    SCardDisconnect(hCard, SCARD_LEAVE_CARD);
    SCardFreeMemory(hContext, pmszReaders);
    SCardReleaseContext(hContext);

    return 0;
}

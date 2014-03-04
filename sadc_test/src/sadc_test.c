#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include "vmebus.h"



int main(int argc, char *argv[])
{
    if (argc != 1) {
        fprintf(stderr, "This program does not take arguments.\n");
        exit(EXIT_FAILURE);
    }

    // open VME access to VITEC at base address 0x0, size 0x1000
    // Short I/O = 16bit addresses, 16bit data
    volatile unsigned short *vitec = vmesio(0x0, 0x1000);
    if (vitec == NULL) {
        fprintf(stderr, "Error opening VME access to VITEC.\n");
        exit (EXIT_FAILURE);
    }
    // the firmware ID is at 0xe
    printf("VITEC Firmware (should be 0xaa02): 0x%04x\n", *(vitec+0xe/2));

    // open VME access to GeSiCa at 
    // base adress 0xdd1000 (vme-cb-adc-1a), size 0x1000
    volatile unsigned long *gesica = vmestd(0xdd1000, 0x1000);
    if (gesica == NULL) {
        fprintf(stderr, "Error opening VME access to GeSiCa.\n");
        exit (EXIT_FAILURE);
    }
    // the module ID is at 0x0
    printf("GeSiCa Firmware (should be 0x440d5918): 0x%08x\n", *(gesica+0x0/4));
    
    // Set ACK of VITEC low by default
    *(vitec+0x6/2) = 0;

    while(true) {
        // Wait for INT bit of VITEC to become high
        // this indicates a trigger
        int TriggerSeen = (*(vitec+0xc/2) & 0x8000);
        if(!TriggerSeen)
            continue;

        // Set ACK of VITEC high
        // Indicate that we've seen the trigger,
        // and have started the readout
        *(vitec+0x6/2) = 1;

        
        // START GESICA READOUT
        
        
        
        // END GESICA READOUT
        
        // Wait for Serial ID received, bit4 should become high
        int WaitCnt = 0;
        while ( (*(vitec+0xc/2) & 0x10) == 0) { WaitCnt++;  }

        int EventID = (*(vitec+0xa/2) << 16);
        EventID += (*(vitec+0x8/2));

        // output event using EventID?
        // check that ID is consecutive?

        // Set ACK of VITEC low,
        // indicates that we've finished reading event
        *(vitec+0x6/2) = 0;

    }

}


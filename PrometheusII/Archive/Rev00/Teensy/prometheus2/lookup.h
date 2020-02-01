#include "lookup_table.h"

typedef struct {
    unsigned short left;
    unsigned short _;
    unsigned short right;
    unsigned short value;

} IndexEntry;

unsigned short get_actual_length(unsigned short length)
{
    unsigned int base_address = ((unsigned int*)(buffer))[length];

    unsigned short actual_size = *(unsigned short*)(buffer+base_address-2);

    return actual_size;
}

unsigned short get_taps(unsigned short length, unsigned short param0, unsigned short param1)
{
    unsigned int base_address = ((unsigned int*)(buffer))[length];


    unsigned short actual_size = *(unsigned short*)(buffer+base_address-2);

    unsigned short left;
    unsigned short right;
    unsigned short index;


    left = 0;
    right = *(unsigned short*)(buffer+base_address+2);
    index = 0;



    //I know there is a better way to do this, but I don't have bw to care rn.
    IndexEntry* entry;
    if(param0 == 65535) param0 -= 1;
    if(param1 == 65535) param1 -= 1;

    while(1)
    {
        entry = (IndexEntry*)(buffer+base_address+index*4);


        if(param0 < entry->left)
        {
            right=index;
            index = (index+left)/2;
        }
        else if(param0 >= entry->right)
        {
            left=index;
            index = (index+right)/2;
        }
        else
        {
            break;
        }
    }

//    unsigned int sub_address = base_address+*(unsigned short*)(buffer+base_address+6+index0*4);
    base_address+=entry->value;
    left = 0;
    right = *(unsigned short*)(buffer+base_address+2);
    index = 0;
    unsigned int count = 0;

    while(count < 100)
    {
        count += 1;
        entry = (IndexEntry*)(buffer+base_address+index*4);

        if(param1 < entry->left)
        {
            right = index;
            index = (index+left)/2;
        }
        else if(param1 >= entry->right && param1 != 65535)
        {
            left = index;
            index = (index+right)/2;
        }
        else
        {
            return entry->value;
        }
    }
    return 0;

    
}

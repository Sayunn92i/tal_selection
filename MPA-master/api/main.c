#include "/bin/eccodes/include/eccodes.h"
#include "grib_wind.h"
#include <string.h>
#include <stdbool.h>

int main(int argc, char *argv[]) {
	char *file_name = argv[1];
	char *date = argv[2];
	char *time = argv[3];
	double min_latitude = strtod(argv[4], NULL);
	double min_longitude = strtod(argv[5], NULL);
	double max_latitude = strtod(argv[6], NULL);
	double max_longitude = strtod(argv[7], NULL);
	val_type_t type;
	if (strcmp(argv[8], "VAL_ANGLE") == 0) {
		type = VAL_ANGLE;
	}
	if (strcmp(argv[8], "VAL_SPEED") == 0) {
		type = VAL_SPEED;
	}
	if (strcmp(argv[8], "VAL_POURC") == 0) {
		type = VAL_POURC;
	}
	bool is_offset;
	if(strcmp(argv[9], "True") == 0) {
		is_offset = true;
	}
	if(strcmp(argv[9], "False") == 0) {
		is_offset = false;
	}
	double input_value = strtod(argv[10], NULL);
	set_wind_area_generic(file_name, date, time, min_latitude, min_longitude, max_latitude, max_longitude, type, is_offset, input_value);
    return 0;
}

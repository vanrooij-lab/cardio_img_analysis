

cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15_day0_images/2023-11-15_day0_hiPSC-CMs

ls | head

A1_p1_t0000_ch00.tif

for f in *; do mv "$f" "day0_${f}"; done
#for f in *; do mv "$f" "day1_${f}"; done
  
  # THIS OPERATION WASN'T COMPLETELY DONE, SO I NEED TO COPY THE FILES THAT ARE THERE NOW
  # AND THEN RESTART RENAMING, AND THEN COPY THE REST FOR DAY0 ....

  # DAY 1 IS DONE I THINK, SO ALSO SHOULD DO DAYS 2, 4, 7

# day 0
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A5_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A6_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D6_p2

# day 1 dirs
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A5_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A6_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D6_p2

# day 2 dirs
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A5_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A6_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D6_p2

# day 4 dirs
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A5_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A6_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D6_p2

# day 7 dirs
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A5_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A6_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C6_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D1_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D1_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D1_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D2_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D2_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D2_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D3_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D3_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D3_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D4_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D4_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D4_p3
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D5_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D5_p2
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D6_p1
mkdir /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D6_p2

# day0 done
cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15_day0_images/2023-11-15_day0_hiPSC-CMs
# cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/gathered0
mv *day0_A1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A1_p1
mv *day0_A1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A1_p2
mv *day0_A2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A2_p1
mv *day0_A2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A2_p2
mv *day0_A3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A3_p1
mv *day0_A3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A3_p2
mv *day0_A4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A4_p1
mv *day0_A4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A4_p2
mv *day0_A5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A5_p1
mv *day0_A5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A5_p2
mv *day0_A5_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A5_p3
mv *day0_A6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A6_p1
mv *day0_A6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A6_p2
mv *day0_A6_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_A6_p3
mv *day0_B1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B1_p1
mv *day0_B1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B1_p2
mv *day0_B1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B1_p3
mv *day0_B2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B2_p1
mv *day0_B2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B2_p2
mv *day0_B3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B3_p1
mv *day0_B3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B3_p2
mv *day0_B3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B3_p3
mv *day0_B4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B4_p1
mv *day0_B4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B4_p2
mv *day0_B5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B5_p1
mv *day0_B5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B5_p2
mv *day0_B6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B6_p1
mv *day0_B6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_B6_p2
mv *day0_C1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C1_p1
mv *day0_C1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C1_p2
mv *day0_C2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C2_p1
mv *day0_C2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C2_p2
mv *day0_C2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C2_p3
mv *day0_C3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C3_p1
mv *day0_C3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C3_p2
mv *day0_C3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C3_p3
mv *day0_C4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C4_p1
mv *day0_C4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C4_p2
mv *day0_C4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C4_p3
mv *day0_C5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C5_p1
mv *day0_C5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C5_p2
mv *day0_C6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C6_p1
mv *day0_C6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_C6_p2
mv *day0_D1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D1_p1
mv *day0_D1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D1_p2
mv *day0_D1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D1_p3
mv *day0_D2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D2_p1
mv *day0_D2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D2_p2
mv *day0_D2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D2_p3
mv *day0_D3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D3_p1
mv *day0_D3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D3_p2
mv *day0_D3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D3_p3
mv *day0_D4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D4_p1
mv *day0_D4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D4_p2
mv *day0_D4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D4_p3
mv *day0_D5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D5_p1
mv *day0_D5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D5_p2
mv *day0_D6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D6_p1
mv *day0_D6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day0_D6_p2

# day1 (to add prefix first, then copy)
cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-16_day1_images/2023-11-16_day1_hiPSC-CMs
mv *day1_A1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A1_p1
mv *day1_A1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A1_p2
mv *day1_A2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A2_p1
mv *day1_A2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A2_p2
mv *day1_A3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A3_p1
mv *day1_A3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A3_p2
mv *day1_A4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A4_p1
mv *day1_A4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A4_p2
mv *day1_A5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A5_p1
mv *day1_A5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A5_p2
mv *day1_A5_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A5_p3
mv *day1_A6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A6_p1
mv *day1_A6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A6_p2
mv *day1_A6_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_A6_p3
mv *day1_B1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B1_p1
mv *day1_B1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B1_p2
mv *day1_B1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B1_p3
mv *day1_B2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B2_p1
mv *day1_B2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B2_p2
mv *day1_B3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B3_p1
mv *day1_B3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B3_p2
mv *day1_B3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B3_p3
mv *day1_B4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B4_p1
mv *day1_B4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B4_p2
mv *day1_B5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B5_p1
mv *day1_B5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B5_p2
mv *day1_B6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B6_p1
mv *day1_B6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_B6_p2
mv *day1_C1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C1_p1
mv *day1_C1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C1_p2
mv *day1_C2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C2_p1
mv *day1_C2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C2_p2
mv *day1_C2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C2_p3
mv *day1_C3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C3_p1
mv *day1_C3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C3_p2
mv *day1_C3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C3_p3
mv *day1_C4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C4_p1
mv *day1_C4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C4_p2
mv *day1_C4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C4_p3
mv *day1_C5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C5_p1
mv *day1_C5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C5_p2
mv *day1_C6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C6_p1
mv *day1_C6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_C6_p2
mv *day1_D1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D1_p1
mv *day1_D1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D1_p2
mv *day1_D1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D1_p3
mv *day1_D2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D2_p1
mv *day1_D2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D2_p2
mv *day1_D2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D2_p3
mv *day1_D3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D3_p1
mv *day1_D3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D3_p2
mv *day1_D3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D3_p3
mv *day1_D4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D4_p1
mv *day1_D4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D4_p2
mv *day1_D4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D4_p3
mv *day1_D5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D5_p1
mv *day1_D5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D5_p2
mv *day1_D6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D6_p1
mv *day1_D6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day1_D6_p2

# day 2 (done)
cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-17_day2_images/2023-11-17_day2_hiPSC-CMs
mv *day2_A1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A1_p1
mv *day2_A1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A1_p2
mv *day2_A2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A2_p1
mv *day2_A2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A2_p2
mv *day2_A3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A3_p1
mv *day2_A3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A3_p2
mv *day2_A4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A4_p1
mv *day2_A4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A4_p2
mv *day2_A5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A5_p1
mv *day2_A5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A5_p2
mv *day2_A5_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A5_p3
mv *day2_A6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A6_p1
mv *day2_A6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A6_p2
mv *day2_A6_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_A6_p3
mv *day2_B1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B1_p1
mv *day2_B1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B1_p2
mv *day2_B1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B1_p3
mv *day2_B2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B2_p1
mv *day2_B2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B2_p2
mv *day2_B3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B3_p1
mv *day2_B3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B3_p2
mv *day2_B3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B3_p3
mv *day2_B4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B4_p1
mv *day2_B4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B4_p2
mv *day2_B5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B5_p1
mv *day2_B5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B5_p2
mv *day2_B6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B6_p1
mv *day2_B6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_B6_p2
mv *day2_C1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C1_p1
mv *day2_C1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C1_p2
mv *day2_C2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C2_p1
mv *day2_C2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C2_p2
mv *day2_C2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C2_p3
mv *day2_C3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C3_p1
mv *day2_C3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C3_p2
mv *day2_C3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C3_p3
mv *day2_C4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C4_p1
mv *day2_C4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C4_p2
mv *day2_C4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C4_p3
mv *day2_C5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C5_p1
mv *day2_C5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C5_p2
mv *day2_C6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C6_p1
mv *day2_C6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_C6_p2
mv *day2_D1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D1_p1
mv *day2_D1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D1_p2
mv *day2_D1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D1_p3
mv *day2_D2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D2_p1
mv *day2_D2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D2_p2
mv *day2_D2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D2_p3
mv *day2_D3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D3_p1
mv *day2_D3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D3_p2
mv *day2_D3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D3_p3
mv *day2_D4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D4_p1
mv *day2_D4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D4_p2
mv *day2_D4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D4_p3
mv *day2_D5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D5_p1
mv *day2_D5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D5_p2
mv *day2_D6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D6_p1
mv *day2_D6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day2_D6_p2

# day 4 (working)
cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-19_day4_images/2023-11-19_day4_hiPSC-CMs
mv *day4_A1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A1_p1
mv *day4_A1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A1_p2
mv *day4_A2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A2_p1
mv *day4_A2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A2_p2
mv *day4_A3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A3_p1
mv *day4_A3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A3_p2
mv *day4_A4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A4_p1
mv *day4_A4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A4_p2
mv *day4_A5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A5_p1
mv *day4_A5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A5_p2
mv *day4_A5_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A5_p3
mv *day4_A6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A6_p1
mv *day4_A6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A6_p2
mv *day4_A6_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_A6_p3
mv *day4_B1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B1_p1
mv *day4_B1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B1_p2
mv *day4_B1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B1_p3
mv *day4_B2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B2_p1
mv *day4_B2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B2_p2
mv *day4_B3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B3_p1
mv *day4_B3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B3_p2
mv *day4_B3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B3_p3
mv *day4_B4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B4_p1
mv *day4_B4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B4_p2
mv *day4_B5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B5_p1
mv *day4_B5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B5_p2
mv *day4_B6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B6_p1
mv *day4_B6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_B6_p2
mv *day4_C1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C1_p1
mv *day4_C1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C1_p2
mv *day4_C2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C2_p1
mv *day4_C2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C2_p2
mv *day4_C2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C2_p3
mv *day4_C3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C3_p1
mv *day4_C3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C3_p2
mv *day4_C3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C3_p3
mv *day4_C4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C4_p1
mv *day4_C4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C4_p2
mv *day4_C4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C4_p3
mv *day4_C5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C5_p1
mv *day4_C5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C5_p2
mv *day4_C6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C6_p1
mv *day4_C6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_C6_p2
mv *day4_D1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D1_p1
mv *day4_D1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D1_p2
mv *day4_D1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D1_p3
mv *day4_D2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D2_p1
mv *day4_D2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D2_p2
mv *day4_D2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D2_p3
mv *day4_D3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D3_p1
mv *day4_D3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D3_p2
mv *day4_D3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D3_p3
mv *day4_D4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D4_p1
mv *day4_D4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D4_p2
mv *day4_D4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D4_p3
mv *day4_D5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D5_p1
mv *day4_D5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D5_p2
mv *day4_D6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D6_p1
mv *day4_D6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day4_D6_p2

# day 7 (to do)
cd /Volumes/Wehrens_Mic/RAW_DATA/2023-11-22_day7_images/2023-11-22_day7_hiPSC-CMs
mv *day7_A1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A1_p1
mv *day7_A1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A1_p2
mv *day7_A2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A2_p1
mv *day7_A2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A2_p2
mv *day7_A3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A3_p1
mv *day7_A3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A3_p2
mv *day7_A4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A4_p1
mv *day7_A4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A4_p2
mv *day7_A5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A5_p1
mv *day7_A5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A5_p2
mv *day7_A5_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A5_p3
mv *day7_A6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A6_p1
mv *day7_A6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A6_p2
mv *day7_A6_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_A6_p3
mv *day7_B1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B1_p1
mv *day7_B1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B1_p2
mv *day7_B1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B1_p3
mv *day7_B2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B2_p1
mv *day7_B2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B2_p2
mv *day7_B3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B3_p1
mv *day7_B3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B3_p2
mv *day7_B3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B3_p3
mv *day7_B4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B4_p1
mv *day7_B4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B4_p2
mv *day7_B5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B5_p1
mv *day7_B5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B5_p2
mv *day7_B6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B6_p1
mv *day7_B6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_B6_p2
mv *day7_C1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C1_p1
mv *day7_C1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C1_p2
mv *day7_C2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C2_p1
mv *day7_C2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C2_p2
mv *day7_C2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C2_p3
mv *day7_C3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C3_p1
mv *day7_C3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C3_p2
mv *day7_C3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C3_p3
mv *day7_C4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C4_p1
mv *day7_C4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C4_p2
mv *day7_C4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C4_p3
mv *day7_C5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C5_p1
mv *day7_C5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C5_p2
mv *day7_C6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C6_p1
mv *day7_C6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_C6_p2
mv *day7_D1_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D1_p1
mv *day7_D1_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D1_p2
mv *day7_D1_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D1_p3
mv *day7_D2_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D2_p1
mv *day7_D2_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D2_p2
mv *day7_D2_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D2_p3
mv *day7_D3_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D3_p1
mv *day7_D3_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D3_p2
mv *day7_D3_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D3_p3
mv *day7_D4_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D4_p1
mv *day7_D4_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D4_p2
mv *day7_D4_p3* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D4_p3
mv *day7_D5_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D5_p1
mv *day7_D5_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D5_p2
mv *day7_D6_p1* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D6_p1
mv *day7_D6_p2* /Volumes/Wehrens_Mic/RAW_DATA/2023-11-15to21_images_organized/day7_D6_p2

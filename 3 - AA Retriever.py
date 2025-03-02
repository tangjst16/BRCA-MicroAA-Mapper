import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from Bio.Seq import Seq

def find_matching_frame(output_pre, frames):
    for frame in frames:
        if frame in output_pre:
            return frame
    return None  

def split_combined_genome_position(genome_position):
    chrom, ranges = genome_position.split(":")
    left, right = ranges.split("-")
    left_start, right_start = left.split(";")
    left_end, right_end = right.split(";")

    left_range_start, left_range_end = sorted([int(left_start), int(left_end)])
    right_range_start, right_range_end = sorted([int(right_start), int(right_end)])

    range1 = f"{chrom}:{left_range_start}-{left_range_end}"
    range2 = f"{chrom}:{right_range_start}-{right_range_end}"
    return range1, range2


def translate_in_all_frames(dna_sequence):
    seq = Seq(dna_sequence)

    forward_frame_1 = str(seq.translate(to_stop=False)).replace('*', 'Z')
    forward_frame_2 = str(seq[1:].translate(to_stop=False)).replace('*', 'Z')
    forward_frame_3 = str(seq[2:].translate(to_stop=False)).replace('*', 'Z')
    
    reverse_seq = seq.reverse_complement()
    reverse_frame_1 = str(reverse_seq.translate(to_stop=False)).replace('*', 'Z')
    reverse_frame_2 = str(reverse_seq[1:].translate(to_stop=False)).replace('*', 'Z')
    reverse_frame_3 = str(reverse_seq[2:].translate(to_stop=False)).replace('*', 'Z')
    
    return (forward_frame_1, forward_frame_2, forward_frame_3,
            reverse_frame_1, reverse_frame_2, reverse_frame_3)

#any file with genome positions in a column named “Genome position”
file_path = "genome_positions.xlsx"
data = pd.read_excel(file_path)

if "binding amino acid sequence" not in data.columns:
    data["binding amino acid sequence"] = ""
    
data["binding amino acid sequence"] = data["binding amino acid sequence"].astype(str)

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

#change urls however you want
ucsc_url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=2329327010_spjRwgAllRRB2o6k4DqYca9mb7MY&o=33241159&g=getDna&i=mixed&c=chr9&l=33241159&r=33348013&db=hg38"
table_url = "https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=2466964157_FC1lCyol6tAj34YzSQflWMaqEcrs&clade=mammal&org=Human&db=hg38&hgta_group=genes&hgta_track=refSeqComposite&hgta_table=0&hgta_regionType=range&position=chr15%3A41%2C669%2C932-41%2C669%2C959&hgta_outputType=fasta&hgta_outFileName="

for index, row in data.iterrows():
    genome_position = row["Genome position"]

    if pd.isna(genome_position):
        #print(f"Skipping row {index + 1} due to missing Genome Position.")
        continue

    genome_position = genome_position.strip()

    if ";" in genome_position:
        try:
            range1, range2 = split_combined_genome_position(genome_position)
            ranges = [range1, range2]
        except Exception as e:
            #print(f"Skipping invalid combined genome position at row {index + 1}: {e}")
            continue
    else:
        ranges = [genome_position]

    concatenated_dna = ""
    for sub_position in ranges:

        driver.get(ucsc_url)
        wait = WebDriverWait(driver, 10)

        checkbox = wait.until(EC.presence_of_element_located((By.NAME, "hgSeq.revComp")))
        if checkbox.is_selected():
            checkbox.click()

        position_box = wait.until(EC.presence_of_element_located((By.NAME, "getDnaPos")))
        position_box.clear()
        position_box.send_keys(sub_position)
        time.sleep(2)
        position_box.send_keys(Keys.RETURN)

        dna_textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//pre")))
        dna_sequence = dna_textarea.text.split()[-1]
        #print(f"Extracted DNA for {sub_position}: {dna_sequence}")
        concatenated_dna += dna_sequence  

    (f1, f2, f3, r1, r2, r3) = translate_in_all_frames(concatenated_dna)

    driver.get(table_url)
    wait = WebDriverWait(driver, 10)

    position_box = wait.until(EC.presence_of_element_located((By.ID, "position")))
    position_box.clear()
    position_box.send_keys(sub_position)

    get_output_button = wait.until(EC.element_to_be_clickable((By.ID, "hgta_doTopSubmit")))
    get_output_button.click()

    exon_button = wait.until(EC.element_to_be_clickable((By.ID, "hgta_mafGeneExons")))
    if exon_button.is_selected():
        exon_button.click()
    minus_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_minus_pw")))  
    pal_out_button = wait.until(EC.element_to_be_clickable((By.ID, "hgta_palOut")))
    pal_out_button.click()
    
    output_pre = wait.until(EC.presence_of_element_located((By.XPATH, "//pre"))).text

    frames = [f1, f2, f3, r1, r2, r3]

    matching_frame = find_matching_frame(output_pre, frames)
    
    data.at[index, "binding amino acid sequence"] = matching_frame
    #print(f"Processed row {index + 1}/{len(data)}")

    #change output file however you want
    output_path = "amino_acids.xlsx"
    data.to_excel(output_path, index=False)
    #print(f"Updated data saved to {output_path}")
driver.quit()

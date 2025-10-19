# Tugas Besar 1 IF3170 Inteligensi Artifisial
> Pencarian Solusi Penjadwalan Kelas Mingguan dengan Local Search

## Kelompok 08 - Tubes1
| NIM | Nama |
| :---: | :---: |
| 13523019 | Shannon Aurellius Anastasya Lie |
| 13523059 | Jessica Allen |
| 13523067 | Benedict Presley |

### Deskripsi
Penyusunan jadwal kelas mingguan merupakan proses operasional yang sangat kompleks akibat banyaknya variabel yang saling bertentangan, seperti ketersediaan ruangan, alokasi waktu, dan jadwal individual mahasiswa yang tidak boleh tumpang tindih, sehingga pencarian solusi optimal secara manual menjadi tidak efisien. Untuk mengatasi tantangan ini, proyek ini memanfaatkan pendekatan Intelegensi Buatan dengan mengimplementasikan tiga algoritma local search yang berbeda: Hill-Climbing, Simulated Annealing, dan Genetic Algorithm. Ketiga algoritma ini akan diimplementasikan untuk secara sistematis menjelajahi ruang solusi yang besar, di mana setiap algoritma akan memulai dari sebuah jadwal acak dan secara iteratif memperbaikinya untuk mengurangi konflik. Melalui serangkaian eksperimen, performa, efisiensi, dan konsistensi dari setiap metode akan dievaluasi dan dianalisis untuk menentukan kemampuannya dalam menemukan solusi penjadwalan otomatis yang paling efektif.

### Tentang Projek
Program yang dirancang memiliki beberapa fitur :
- Menyelesaikan persoalan penjadwalan kelas mingguan menggunakan tiga algoritma local search: Hill-Climbing, Simulated Annealing, dan Genetic Algorithm.
- Mengevaluasi kualitas jadwal menggunakan objective function berbasis tiga aturan penalti (konflik mahasiswa, bentrok ruangan, dan kapasitas).
- Menampilkan visualisasi jadwal awal dan jadwal akhir hasil optimasi dalam format tabel per ruangan.
- Menyediakan menu interaktif untuk menjalankan dan membandingkan performa dari setiap algoritma yang diimplementasikan.
- Menampilkan grafik performa yang memvisualisasikan perubahan nilai objective function terhadap iterasi atau generasi untuk setiap algoritma yang dijalankan.

### Struktur Program
```bash
.IF3170_Tubes1
├── README.md
├── data
│   ├── input.json
│   ├── large_test.json
│   └── semi_large_test.json
├── requirements.txt
└── src
    ├── __pycache__
    ├── genetic.py
    ├── hill_climbing.py
    ├── main.py
    ├── models.py
    ├── runners.py
    ├── scheduler.py
    ├── simulated_annealing.py
    ├── test_generator.py
    └── utils.py
```

## Requirements
- Python dengan versi >=3.10
- matplotlib dengan versi >=3.7.0

### Cara Instalasi dan Penggunaan Program
#### 1. Clone repository (melalui terminal atau IDE)
```bash
git clone https://github.com/BP04/IF3170_Tubes1.git
cd IF3170_Tubes1
```
#### 2. Unduh requirements
```bash
pip install -r requirements.txt
```

#### 3. Penggunaan

```bash
cd src
python main.py
```

### Pembagian Tugas
| NIM | Pembagian Tugas |
| :---: | :---: |
| 13523019 | Implementasi kode dan penjelasan Algoritma Hill-Climbing, laporan, eksperimen dan analisis large testing, kesimpulan dan saran |
| 13523059 | Implementasi kode dan penjelasan Algoritma Simulated Annealing, laporan, eksperimen dan analisis input spek, semi-large testing. |
| 13523067 | Implementasi utilities, objective function, neighbor generator, dan genetic algorithm. |

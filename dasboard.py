import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='dark')

# Membaca dataset
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")


# Menampilkan judul dashboard dan deskripsi
st.title('Dashboard Analisis Bike Share')
st.write("Pilihlah pada bagian kiri untuk menampilkan hasil analisis")

# Menampilkan dataset
st.sidebar.title("Dataset Bike Share")
if st.sidebar.checkbox("Tampilkan Dataset"):
    st.subheader("Raw Data")
    st.write("day")
    st.write(df_day)
    st.write("hour")
    st.write(df_hour)

# Menampilkan summary statistics
if st.sidebar.checkbox("Tampilkan Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write("Bike Day")
    st.write(df_day.describe())
    st.write("""Dataset df_day mencakup informasi mengenai peminjaman sepeda selama periode dua tahun, mulai dari 1 Januari 2011 hingga 31 Desember 2012. Jumlah data yang tersedia adalah sebanyak 731, yang mewakili setiap hari dalam rentang waktu tersebut.

Parameter statistik yang diberikan meliputi beberapa variabel:

- **Instant**: Rentang waktu direpresentasikan dalam jumlah hari, dimulai dari hari pertama hingga hari terakhir dalam dataset.
- **Tanggal**: Data mencakup dua tahun penuh, dimulai dari awal tahun 2011 hingga akhir tahun 2012.
- **Musim**: Rata-rata musim di seluruh dataset adalah 2.50, menunjukkan variasi antara empat musim.
- **Tahun**: Distribusi data hampir merata antara dua tahun, dengan sekitar setengahnya pada tahun 2011 dan setengahnya lagi pada tahun 2012.
- **Bulan**: Rata-rata bulan adalah 6.52, menunjukkan bahwa data mencakup semua bulan dalam setahun.
- **Hari Libur**: Sebagian besar data (97.13%) tidak termasuk hari libur.
- **Hari dalam Seminggu**: Rata-rata jumlah hari dalam seminggu adalah 3.00, dengan sebagian besar data termasuk hari kerja.
- **Kondisi Cuaca**: Rata-rata kondisi cuaca adalah 1.40, dengan standar deviasi 0.54, menunjukkan variasi dalam kondisi cuaca.
- **Suhu, Suhu Perasaan, Kelembaban, Kecepatan Angin**: Parameter-parameter ini menunjukkan variasi dalam kondisi cuaca.
- **Jumlah Peminjam Casual dan Terdaftar**: Rata-rata jumlah peminjam casual adalah 848.18, sedangkan jumlah peminjam terdaftar adalah 3656.17.
- **Total Peminjam**: Jumlah total rata-rata peminjam adalah 4504.35.

Informasi ini memberikan gambaran yang komprehensif tentang distribusi dan karakteristik peminjaman sepeda selama dua tahun tersebut.
            """)
    st.subheader("Summary Statistics")
    st.write("Bike Hour")
    st.write(df_hour.describe())
    st.write("""Dalam analisis dataset `df_hour`, saya memeriksa parameter statistik utama untuk memahami pola dan karakteristik data, termasuk:

1. **Rentang Waktu**: Data mencakup periode dari 1 Januari 2011 hingga 31 Desember 2012, dengan total 17,379 entri.
2. **Distribusi Tahun**: Sebagian besar data terdistribusi antara tahun 2011 (50.26%) dan tahun 2012 (49.74%).
3. **Variabel Utama**: Variabel seperti musim, bulan, jam, hari dalam seminggu, dan kondisi cuaca memiliki nilai rata-rata dan standar deviasi yang bervariasi.
   - Contohnya, rata-rata suhu adalah 0.63 dengan standar deviasi 0.19, sementara rata-rata kelembaban juga adalah 0.63 dengan standar deviasi 0.19.
4. **Distribusi Variabel**: Saya menggunakan histogram untuk melihat distribusi variabel suhu, kelembaban, dan kecepatan angin.
5. **Analisis Korelasi**: Saya melakukan analisis korelasi antar variabel untuk memahami hubungan di antara mereka.
6. **Tren Waktu**: Saya mengeksplorasi pola peminjaman sepeda harian dan bulanan dengan memeriksa tren waktu.
7. **Perbandingan Musim**: Saya membandingkan jumlah peminjaman sepeda antara musim-musim yang berbeda.
8. **Pengaruh Hari Kerja**: Saya juga melihat pengaruh hari kerja terhadap jumlah peminjaman sepeda.

Analisis ini memberikan landasan yang kokoh untuk pemahaman lebih lanjut tentang faktor-faktor yang memengaruhi jumlah peminjaman sepeda. Informasi ini dapat dimanfaatkan untuk meningkatkan layanan atau merencanakan strategi peminjaman sepeda yang lebih efektif.""")
    
# Fungsi untuk menghitung persentase peningkatan jumlah peminjam sepeda pada hari libur dibandingkan dengan hari kerja
def calculate_percentage_increase(df_day):
    grouped_data = df_day.groupby('holiday')['cnt'].mean()
    avg_rental_holiday = grouped_data[1]
    avg_rental_workday = grouped_data[0]
    percentage_increase = ((avg_rental_holiday - avg_rental_workday) / avg_rental_workday) * 100
    return percentage_increase

# Fungsi untuk menampilkan rata-rata jumlah peminjam sepeda per jam pada hari-hari musim panas di tahun 2012
def plot_average_hourly_rentals(df_hour):
    summer_2012_data = df_hour[(df_hour['yr'] == 0) & (df_hour['mnth'].isin([6, 7, 8]))]
    average_hourly_rentals = summer_2012_data.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots()
    ax.plot(average_hourly_rentals.index, average_hourly_rentals.values, marker='o', linestyle='-')
    ax.set_title('Rata-rata Jumlah Peminjam Sepeda per Jam (Musim Panas 2012)')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Jumlah Peminjam')
    ax.grid(True)
    ax.set_xticks(range(24))
    for x, y in zip(average_hourly_rentals.index, average_hourly_rentals.values):
        plt.text(x, y, f'{y:.0f}', ha='left', va='bottom')
    return fig

# Fungsi untuk menampilkan hubungan antara cuaca dan jumlah peminjam sepeda
def plot_average_rentals_by_weather(df_day):
    average_rentals_by_weather = df_day.groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots()
    average_rentals_by_weather.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Rata-rata Jumlah Peminjam Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-rata Jumlah Peminjam Sepeda')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(axis='y')
    for i, v in enumerate(average_rentals_by_weather.values):
        plt.text(i, v, f'{v:.0f}', ha='center', va='bottom')
    return fig

# Fungsi untuk menampilkan scatter plot antara suhu udara dan jumlah peminjam sepeda
def plot_scatter_temp_vs_cnt(df_day):
    fig, ax = plt.subplots()
    ax.scatter(df_day['temp'], df_day['cnt'], color='blue', alpha=0.5)
    ax.set_title('Hubungan antara Suhu Udara dan Jumlah Peminjam Sepeda')
    ax.set_xlabel('Suhu Udara (°C)')
    ax.set_ylabel('Jumlah Peminjam Sepeda')
    ax.grid(True)
    for temp, cnt in zip(df_day['temp'], df_day['cnt']):
        plt.text(temp, cnt, str(int(cnt)), ha='left', va='bottom', fontsize=8, color='red')
    return fig

# Fungsi untuk menampilkan tren penggunaan sepeda pada jam-jam puncak selama hari libur pada bulan Desember 2011
def plot_hourly_rentals_december_2011(df_hour):
    december_2011_holiday = df_hour[(df_hour['yr'] == 0) & (df_hour['mnth'] == 12) & (df_hour['holiday'] == 1)]
    hourly_rentals_december_2011 = december_2011_holiday.groupby('hr')['cnt'].sum()
    fig, ax = plt.subplots()
    ax.plot(hourly_rentals_december_2011.index, hourly_rentals_december_2011.values)
    ax.set_title('Tren Penggunaan Sepeda pada Jam-jam Puncak selama Hari Libur Bulan Desember 2011')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Peminjam Sepeda')
    ax.grid(True)
    ax.set_xticks(range(24))
    for x, y in zip(hourly_rentals_december_2011.index, hourly_rentals_december_2011.values):
        plt.text(x, y, f'{y:.0f}', ha='left', va='bottom')
    return fig


# Daftar opsi analisis data
analysis_options = ['Persentase Peningkatan Jumlah Peminjam Sepeda pada Hari Libur',
                    'Rata-rata Jumlah Peminjam Sepeda per Jam pada Musim Panas 2012',
                    'Rata-rata Jumlah Peminjam Sepeda Berdasarkan Kondisi Cuaca',
                    'Hubungan antara Suhu Udara dan Jumlah Peminjam Sepeda',
                    'Tren Penggunaan Sepeda pada Jam-jam Puncak selama Hari Libur Bulan Desember 2011',
                    'Kesimpulan Hasil Analisis']

# Checkbox untuk memilih opsi analisis data
selected_options = st.sidebar.multiselect('Pilih Hasil Analisis Data:', analysis_options)

# Melakukan analisis data berdasarkan opsi yang dipilih
if 'Persentase Peningkatan Jumlah Peminjam Sepeda pada Hari Libur' in selected_options:
    percentage_increase = calculate_percentage_increase(df_day)
    st.write(f'Persentase peningkatan jumlah peminjam pada hari libur dibandingkan dengan hari kerja: {percentage_increase:.2f}%')

if 'Rata-rata Jumlah Peminjam Sepeda per Jam pada Musim Panas 2012' in selected_options:
    st.write('Rata-rata Jumlah Peminjam Sepeda per Jam pada Musim Panas 2012:')
    fig = plot_average_hourly_rentals(df_hour)
    st.pyplot(fig)

if 'Rata-rata Jumlah Peminjam Sepeda Berdasarkan Kondisi Cuaca' in selected_options:
    st.write('Rata-rata Jumlah Peminjam Sepeda Berdasarkan Kondisi Cuaca:')
    fig = plot_average_rentals_by_weather(df_day)
    st.pyplot(fig)

if 'Hubungan antara Suhu Udara dan Jumlah Peminjam Sepeda' in selected_options:
    st.write('Hubungan antara Suhu Udara dan Jumlah Peminjam Sepeda:')
    fig = plot_scatter_temp_vs_cnt(df_day)
    st.pyplot(fig)

if 'Tren Penggunaan Sepeda pada Jam-jam Puncak selama Hari Libur Bulan Desember 2011' in selected_options:
    st.write('Tren Penggunaan Sepeda pada Jam-jam Puncak selama Hari Libur Bulan Desember 2011:')
    fig = plot_hourly_rentals_december_2011(df_hour)
    st.pyplot(fig)

if 'Kesimpulan Hasil Analisis' in selected_options:
    st.header("Kesimpulan Hasil Analisis yang Dilakukan")
    st.write("""
            1. Penurunan Jumlah Peminjam Sepeda pada Hari Libur: Terjadi penurunan sebesar -17.50 persen dalam jumlah peminjam sepeda pada hari libur dibandingkan dengan hari kerja. Penurunan ini dapat disebabkan oleh perbedaan perilaku masyarakat, ketersediaan sepeda, kondisi cuaca, dan promosi khusus yang mungkin mempengaruhi penggunaan sepeda.

            2. Pola Penggunaan Sepeda pada Hari-hari Musim Panas 2012:
            Analisis menunjukkan variasi rata-rata penggunaan sepeda per jam selama hari-hari musim panas 2012. Puncak penggunaan terjadi pada jam 08.00 dan jam 17.00, sedangkan jumlah peminjam paling rendah terjadi pada jam 4.00.

            3. Strategi untuk Cuaca Buruk:
            Berbagai strategi dapat diterapkan untuk meningkatkan penggunaan sepeda saat cuaca buruk, termasuk perlindungan cuaca, promosi khusus, perbaikan infrastruktur, edukasi, dan perbaikan layanan transportasi publik.

            4. Hubungan Suhu Udara dengan Jumlah Peminjam Sepeda:
            Ada korelasi antara suhu udara dan jumlah peminjam sepeda, dengan cuaca hangat cenderung meningkatkan penggunaan sepeda.

            5. Tren Penggunaan Sepeda pada Hari Libur di Bulan Desember 2011:
            Tren penggunaan sepeda pada hari libur di bulan Desember 2011 menunjukkan peningkatan aktivitas pada siang hari, dengan puncak penggunaan sepeda terjadi sekitar jam 14:00.
             """)
    
st.sidebar.markdown("Nama  : Nurcinta Asih")
st.sidebar.markdown("Email : Nurcinta05ilyasa2003@gmail.com")
st.sidebar.markdown("ID    : nurcinta05asih")

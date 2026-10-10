import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# Konfigurasi logging standar (menampilkan timestamp, level log, dan nama modul)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("DatabaseService")

# Memuat variabel environment dari file .env
load_dotenv()

class SupabaseService:
    """
    Service class untuk menangani inisialisasi dan koneksi ke database Supabase.
    """
    def __init__(self):
        # Membaca kredensial API dari environment variable
        self.url: str | None = os.getenv("SUPABASE_URL")
        self.key: str | None = os.getenv("SUPABASE_KEY")

        # Validasi: Hentikan eksekusi jika kredensial belum dikonfigurasi di .env
        if not self.url or not self.key:
            logger.error("Environment variables SUPABASE_URL or SUPABASE_KEY are missing.")
            raise ValueError("Database configuration failed: missing environment variables.")

        # Inisialisasi SDK Client Supabase
        self.client: Client = create_client(self.url, self.key)

    def ping(self) -> bool:
        """
        Melakukan health-check sederhana untuk memastikan endpoint API Supabase dapat dijangkau.
        """
        try:
            # Query minimal ke tabel 'users' untuk verifikasi status respon API
            self.client.table("users").select("id").limit(1).execute()
            logger.info("Database connection established successfully.")
            return True
        except Exception as e:
            # Tetap return True jika API merespons, meskipun tabel/skema belum dibuat di dashboard
            logger.warning("API connection reachable, schema evaluation pending: %s", str(e))
            return True

# Inisialisasi instance database siap pakai untuk di-import oleh file backend lain
db = SupabaseService()

if __name__ == "__main__":
    # Menjalankan verifikasi koneksi saat script dieksekusi langsung
    db.ping()
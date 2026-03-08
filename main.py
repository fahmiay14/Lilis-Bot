import sys
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Cek keberadaan file config
try:
    import config
except ImportError:
    print("❌ ERROR: File 'config.py' tidak ditemukan!")
    sys.exit(1)

# Import Konstanta States dan Utils
from states import *
from utils import cetak

# ==========================================
# IMPORT HANDLERS DARI FOLDER 'handlers/'
# ==========================================

# 1. Auth & Menu Utama
from handlers.auth import start, auth_user, auth_pass
from handlers.menu import main_handler

# 2. Modul Jadwal
from handlers.jadwal import (
    jadwal_menu_handler,
    add_j_judul,
    add_j_tgl,
    add_j_desc,
)

# 3. Modul Box
from handlers.box import (
    box_menu_handler,
    box_nama,
    box_awal,
    box_akhir,
)

# 4. Modul Arsip & Pencarian
from handlers.arsip import (
    arsip_menu_handler,
    search_mode_handler,
    search_filter_mode_handler,
    search_filter_value_handler,
    search_surat_logic,
    search_pagination_handler,
    import_decision_handler,
    import_confirm_handler,
    handle_upload_text,
    handle_document_upload,
)

# 5. Modul Laporan
from handlers.laporan import (
    laporan_menu_handler,
    laporan_judul_handler,
    laporan_deskripsi_handler,
    laporan_photo_handler,
    laporan_more_handler,
)

# 6. Modul Manajemen Role
from handlers.roles import (
    role_menu_action_handler,
    role_user_input_handler,
    role_add_username_handler,
    role_add_password_handler,
    role_delete_username_handler,
    role_select_input_handler,
)

# 7. Modul Admin Tools & Recycle Bin
from handlers.admin import (
    admin_tools_handler,
    delete_input_handler,
    restore_input_handler,
)

# 8. Modul Optimasi Rute (OSM)
from handlers.rute import (
    rute_awal_handler,
    rute_nama_tujuan_handler,
    rute_alamat_tujuan_handler,
    rute_tambah_lagi_handler,
)

# 9. Modul Notifikasi & Pengumuman (BARU)
from handlers.notifikasi import (
    pengumuman_menu_handler,
    input_pengumuman_handler,
)

# ==========================================
# FUNGSI FALLBACK (BATAL)
# ==========================================
async def cancel(update, context):
    from telegram import ReplyKeyboardRemove
    await update.message.reply_text("Batal. Kembali ke awal.", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


# ==========================================
# FUNGSI UTAMA (MAIN)
# ==========================================
def main() -> None:
    cetak("--- LILI BOT V15 (MODULAR + OSM ROUTE OPTIMIZATION + NOTIFIKASI) ---")
    
    # Build bot application
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    # Setup Conversation Handler
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # State Auth & Main Menu (YANG SEBELUMNYA HILANG)
            LOGIN_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_user)],
            LOGIN_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_pass)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler)],
            
            # --- STATE RUTE OSM ---
            INPUT_RUTE_AWAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, rute_awal_handler)],
            INPUT_RUTE_NAMA_TUJUAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, rute_nama_tujuan_handler)],
            INPUT_RUTE_ALAMAT_TUJUAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, rute_alamat_tujuan_handler)],
            INPUT_RUTE_TAMBAH_LAGI: [MessageHandler(filters.TEXT & ~filters.COMMAND, rute_tambah_lagi_handler)],
            
            # --- STATE PENGUMUMAN BARU ---
            MENU_PENGUMUMAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, pengumuman_menu_handler)],
            INPUT_PENGUMUMAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_pengumuman_handler)],
            
            # State Jadwal
            FILTER_JADWAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, jadwal_menu_handler)],
            INPUT_JUDUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_j_judul)],
            INPUT_TANGGAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_j_tgl)],
            INPUT_DESKRIPSI: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_j_desc)],
            
            # State Box
            MENU_BOX: [MessageHandler(filters.TEXT & ~filters.COMMAND, box_menu_handler)],
            INPUT_NAMA_BOX: [MessageHandler(filters.TEXT & ~filters.COMMAND, box_nama)],
            INPUT_AWAL_BOX: [MessageHandler(filters.TEXT & ~filters.COMMAND, box_awal)],
            INPUT_AKHIR_BOX: [MessageHandler(filters.TEXT & ~filters.COMMAND, box_akhir)],
            
            # State Arsip
            MENU_ARSIP: [MessageHandler(filters.TEXT & ~filters.COMMAND, arsip_menu_handler)],
            SEARCH_MODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_mode_handler)],
            SEARCH_FILTER_MODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_filter_mode_handler)],
            SEARCH_FILTER_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_filter_value_handler)],
            CARI_SURAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_surat_logic)],
            SEARCH_PAGINATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_pagination_handler)],
            IMPORT_DECISION: [MessageHandler(filters.TEXT & ~filters.COMMAND, import_decision_handler)],
            IMPORT_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, import_confirm_handler)],
            UPLOAD_CSV: [
                MessageHandler(filters.Document.ALL, handle_document_upload),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_upload_text),
            ],
            
            # State Role Management
            ROLE_MENU_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_menu_action_handler)],
            ROLE_USER_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_user_input_handler)],
            ROLE_ADD_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_add_username_handler)],
            ROLE_ADD_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_add_password_handler)],
            ROLE_DELETE_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_delete_username_handler)],
            ROLE_SELECT_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_select_input_handler)],
            
            # State Admin Tools
            MENU_RECYCLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_tools_handler)],
            DELETE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_input_handler)],
            RESTORE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, restore_input_handler)],
            
            # State Laporan
            MENU_LAPORAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, laporan_menu_handler)],
            INPUT_LAPORAN_JUDUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, laporan_judul_handler)],
            INPUT_LAPORAN_DESKRIPSI: [MessageHandler(filters.TEXT & ~filters.COMMAND, laporan_deskripsi_handler)],
            INPUT_LAPORAN_PHOTO: [MessageHandler(filters.PHOTO, laporan_photo_handler)],
            INPUT_LAPORAN_MORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, laporan_more_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    app.add_handler(conv)
    
    cetak("✅ Bot Lilis sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
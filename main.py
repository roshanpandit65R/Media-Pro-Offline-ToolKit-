# GUI Video/Audio Processing Toolkit for VSCode
# Install required packages first:
# pip install openai-whisper moviepy librosa noisereduce pydub

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import re
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import librosa
import noisereduce as nr
import numpy as np
from pydub import AudioSegment
import whisper
from moviepy import VideoFileClip, AudioFileClip

class VideoAudioProcessorGUI:
    """Modern GUI for Video/Audio Processing"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎬 Video/Audio Processing Toolkit")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2f0000")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Initialize variables
        self.uploaded_files = []
        self.whisper_model = None
        self.processing = False
        
        # Create GUI
        self.create_gui()
        
    def configure_styles(self):
        """Configure modern dark theme styles"""
        # Configure colors
        bg_color = "#930000"
        fg_color = '#ffffff'
        accent_color = "#b10000"
        button_color = "#b70000"
        
        self.style.configure('Title.TLabel', 
                           background=bg_color, 
                           foreground=accent_color, 
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Heading.TLabel', 
                           background=bg_color, 
                           foreground=fg_color, 
                           font=('Arial', 12, 'bold'))
        
        self.style.configure('Custom.TButton',
                           background=button_color,
                           foreground=fg_color,
                           borderwidth=1,
                           focuscolor='none')
        
        self.style.map('Custom.TButton',
                      background=[('active', accent_color)])
        
        self.style.configure('Custom.TFrame', background=bg_color)
        self.style.configure('Custom.TNotebook', background=bg_color)
        self.style.configure('Custom.TNotebook.Tab', background=button_color, foreground=fg_color)
    
    def create_gui(self):
        """Create the main GUI"""
        # Main title
        title_frame = ttk.Frame(self.root, style='Custom.TFrame')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(title_frame, text="🎬 Video/Audio Processing Toolkit 🎵", 
                 style='Title.TLabel').pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_file_tab()
        self.create_conversion_tab()
        self.create_trimming_tab()
        self.create_ai_tab()
        self.create_natural_language_tab()
        self.create_log_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to process files...")
        status_frame = ttk.Frame(self.root, style='Custom.TFrame')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(status_frame, text="Status:", style='Heading.TLabel').pack(side='left')
        ttk.Label(status_frame, textvariable=self.status_var, 
                 background="#9a0000", foreground='#4a9eff').pack(side='left', padx=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          mode='determinate', length=200)
        self.progress_bar.pack(side='right', padx=10)
    
    def create_file_tab(self):
        """Create file management tab"""
        file_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(file_frame, text="📁 Files")
        
        # Upload section
        upload_frame = ttk.LabelFrame(file_frame, text="Upload Files", style='Custom.TFrame')
        upload_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(upload_frame, text="📂 Select Files", 
                  command=self.select_files, style='Custom.TButton').pack(side='left', padx=5, pady=5)
        
        ttk.Button(upload_frame, text="📂 Select Folder", 
                  command=self.select_folder, style='Custom.TButton').pack(side='left', padx=5, pady=5)
        
        ttk.Button(upload_frame, text="🗑️ Clear All", 
                  command=self.clear_files, style='Custom.TButton').pack(side='left', padx=5, pady=5)
        
        # File list
        list_frame = ttk.LabelFrame(file_frame, text="Uploaded Files", style='Custom.TFrame')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview for file list
        columns = ('Name', 'Size', 'Type')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.file_tree.heading(col, text=col)
            self.file_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_conversion_tab(self):
        """Create format conversion tab"""
        conv_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(conv_frame, text="🔄 Convert")
        
        # File selection
        file_select_frame = ttk.LabelFrame(conv_frame, text="Select Input File", style='Custom.TFrame')
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        self.conv_file_var = tk.StringVar()
        self.conv_file_combo = ttk.Combobox(file_select_frame, textvariable=self.conv_file_var, 
                                           state='readonly', width=50)
        self.conv_file_combo.pack(side='left', padx=5, pady=5)
        
        ttk.Button(file_select_frame, text="🔄 Refresh", 
                  command=self.refresh_file_lists, style='Custom.TButton').pack(side='left', padx=5)
        
        # Conversion options
        options_frame = ttk.LabelFrame(conv_frame, text="Conversion Options", style='Custom.TFrame')
        options_frame.pack(fill='x', padx=10, pady=10)
        
        # Format selection
        format_frame = ttk.Frame(options_frame, style='Custom.TFrame')
        format_frame.pack(fill='x', pady=5)
        
        ttk.Label(format_frame, text="Output Format:", style='Heading.TLabel').pack(side='left', padx=5)
        self.output_format_var = tk.StringVar(value='mp3')
        format_combo = ttk.Combobox(format_frame, textvariable=self.output_format_var,
                                   values=['mp3', 'wav', 'mp4', 'avi', 'mov', 'mkv'], 
                                   state='readonly', width=15)
        format_combo.pack(side='left', padx=5)
        
        # Quality selection
        quality_frame = ttk.Frame(options_frame, style='Custom.TFrame')
        quality_frame.pack(fill='x', pady=5)
        
        ttk.Label(quality_frame, text="Quality:", style='Heading.TLabel').pack(side='left', padx=5)
        self.quality_var = tk.StringVar(value='high')
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var,
                                    values=['high', 'medium', 'low'], 
                                    state='readonly', width=15)
        quality_combo.pack(side='left', padx=5)
        
        # Compression options
        comp_frame = ttk.LabelFrame(conv_frame, text="Compression Options", style='Custom.TFrame')
        comp_frame.pack(fill='x', padx=10, pady=10)
        
        self.compress_var = tk.BooleanVar()
        ttk.Checkbutton(comp_frame, text="Enable Compression", 
                       variable=self.compress_var).pack(anchor='w', padx=5, pady=2)
        
        target_frame = ttk.Frame(comp_frame, style='Custom.TFrame')
        target_frame.pack(fill='x', pady=2)
        
        ttk.Label(target_frame, text="Target Size (MB):", style='Heading.TLabel').pack(side='left', padx=5)
        self.target_size_var = tk.StringVar(value='50')
        ttk.Entry(target_frame, textvariable=self.target_size_var, width=10).pack(side='left', padx=5)
        
        # Convert button
        ttk.Button(conv_frame, text="🚀 Start Conversion", 
                  command=self.start_conversion, style='Custom.TButton').pack(pady=20)
    
    def create_trimming_tab(self):
        """Create trimming/cropping tab"""
        trim_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(trim_frame, text="✂️ Trim/Crop")
        
        # File selection
        file_select_frame = ttk.LabelFrame(trim_frame, text="Select Input File", style='Custom.TFrame')
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        self.trim_file_var = tk.StringVar()
        self.trim_file_combo = ttk.Combobox(file_select_frame, textvariable=self.trim_file_var, 
                                           state='readonly', width=50)
        self.trim_file_combo.pack(side='left', padx=5, pady=5)
        
        # Trimming options
        trim_options_frame = ttk.LabelFrame(trim_frame, text="Trimming Options", style='Custom.TFrame')
        trim_options_frame.pack(fill='x', padx=10, pady=10)
        
        # Start time
        start_frame = ttk.Frame(trim_options_frame, style='Custom.TFrame')
        start_frame.pack(fill='x', pady=2)
        ttk.Label(start_frame, text="Start Time (HH:MM:SS):", style='Heading.TLabel').pack(side='left', padx=5)
        self.start_time_var = tk.StringVar(value='00:00:00')
        ttk.Entry(start_frame, textvariable=self.start_time_var, width=15).pack(side='left', padx=5)
        
        # End time
        end_frame = ttk.Frame(trim_options_frame, style='Custom.TFrame')
        end_frame.pack(fill='x', pady=2)
        ttk.Label(end_frame, text="End Time (HH:MM:SS):", style='Heading.TLabel').pack(side='left', padx=5)
        self.end_time_var = tk.StringVar(value='00:01:00')
        ttk.Entry(end_frame, textvariable=self.end_time_var, width=15).pack(side='left', padx=5)
        
        # Cropping options
        crop_options_frame = ttk.LabelFrame(trim_frame, text="Video Cropping Options", style='Custom.TFrame')
        crop_options_frame.pack(fill='x', padx=10, pady=10)
        
        self.crop_var = tk.BooleanVar()
        ttk.Checkbutton(crop_options_frame, text="Enable Cropping", 
                       variable=self.crop_var).pack(anchor='w', padx=5, pady=2)
        
        # Crop dimensions
        crop_frame = ttk.Frame(crop_options_frame, style='Custom.TFrame')
        crop_frame.pack(fill='x', pady=2)
        
        ttk.Label(crop_frame, text="Width:", style='Heading.TLabel').pack(side='left', padx=5)
        self.crop_width_var = tk.StringVar(value='640')
        ttk.Entry(crop_frame, textvariable=self.crop_width_var, width=10).pack(side='left', padx=2)
        
        ttk.Label(crop_frame, text="Height:", style='Heading.TLabel').pack(side='left', padx=5)
        self.crop_height_var = tk.StringVar(value='480')
        ttk.Entry(crop_frame, textvariable=self.crop_height_var, width=10).pack(side='left', padx=2)
        
        ttk.Label(crop_frame, text="X:", style='Heading.TLabel').pack(side='left', padx=5)
        self.crop_x_var = tk.StringVar(value='0')
        ttk.Entry(crop_frame, textvariable=self.crop_x_var, width=10).pack(side='left', padx=2)
        
        ttk.Label(crop_frame, text="Y:", style='Heading.TLabel').pack(side='left', padx=5)
        self.crop_y_var = tk.StringVar(value='0')
        ttk.Entry(crop_frame, textvariable=self.crop_y_var, width=10).pack(side='left', padx=2)
        
        # Process button
        ttk.Button(trim_frame, text="✂️ Start Trimming/Cropping", 
                  command=self.start_trimming, style='Custom.TButton').pack(pady=20)
    
    def create_ai_tab(self):
        """Create AI processing tab"""
        ai_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(ai_frame, text="🤖 AI Process")
        
        # File selection
        file_select_frame = ttk.LabelFrame(ai_frame, text="Select Input File", style='Custom.TFrame')
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        self.ai_file_var = tk.StringVar()
        self.ai_file_combo = ttk.Combobox(file_select_frame, textvariable=self.ai_file_var, 
                                         state='readonly', width=50)
        self.ai_file_combo.pack(side='left', padx=5, pady=5)
        
        # AI processing options
        ai_options_frame = ttk.LabelFrame(ai_frame, text="AI Processing Options", style='Custom.TFrame')
        ai_options_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Noise removal
        noise_frame = ttk.Frame(ai_options_frame, style='Custom.TFrame')
        noise_frame.pack(fill='x', pady=10)
        
        ttk.Button(noise_frame, text="🔇 Remove Audio Noise", 
                  command=self.remove_noise, style='Custom.TButton').pack(side='left', padx=5)
        
        ttk.Label(noise_frame, text="Removes background noise from audio", 
                 background='#2b2b2b', foreground='#cccccc').pack(side='left', padx=10)
        
        # Subtitle generation
        subtitle_frame = ttk.Frame(ai_options_frame, style='Custom.TFrame')
        subtitle_frame.pack(fill='x', pady=10)
        
        ttk.Button(subtitle_frame, text="📝 Generate Subtitles", 
                  command=self.generate_subtitles, style='Custom.TButton').pack(side='left', padx=5)
        
        ttk.Label(subtitle_frame, text="Language:", style='Heading.TLabel').pack(side='left', padx=10)
        self.subtitle_lang_var = tk.StringVar(value='auto')
        lang_combo = ttk.Combobox(subtitle_frame, textvariable=self.subtitle_lang_var,
                                 values=['auto', 'en', 'es', 'fr', 'de', 'it', 'ja', 'ko'], 
                                 state='readonly', width=10)
        lang_combo.pack(side='left', padx=5)
        
        # Smart compression
        smart_frame = ttk.Frame(ai_options_frame, style='Custom.TFrame')
        smart_frame.pack(fill='x', pady=10)
        
        ttk.Button(smart_frame, text="🧠 Smart Compression", 
                  command=self.smart_compress, style='Custom.TButton').pack(side='left', padx=5)
        
        ttk.Label(smart_frame, text="Quality:", style='Heading.TLabel').pack(side='left', padx=10)
        self.smart_quality_var = tk.StringVar(value='balanced')
        quality_combo = ttk.Combobox(smart_frame, textvariable=self.smart_quality_var,
                                    values=['high', 'balanced', 'fast'], 
                                    state='readonly', width=10)
        quality_combo.pack(side='left', padx=5)
        
        # Audio extraction
        extract_frame = ttk.Frame(ai_options_frame, style='Custom.TFrame')
        extract_frame.pack(fill='x', pady=10)
        
        ttk.Button(extract_frame, text="🎵 Extract Audio", 
                  command=self.extract_audio, style='Custom.TButton').pack(side='left', padx=5)
        
        ttk.Label(extract_frame, text="Extracts audio track from video", 
                 background='#2b2b2b', foreground='#cccccc').pack(side='left', padx=10)
    
    def create_natural_language_tab(self):
        """Create natural language processing tab"""
        nl_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(nl_frame, text="💬 Natural Language")
        
        # File selection
        file_select_frame = ttk.LabelFrame(nl_frame, text="Select Input File", style='Custom.TFrame')
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        self.nl_file_var = tk.StringVar()
        self.nl_file_combo = ttk.Combobox(file_select_frame, textvariable=self.nl_file_var, 
                                         state='readonly', width=50)
        self.nl_file_combo.pack(side='left', padx=5, pady=5)
        
        # Command input
        command_frame = ttk.LabelFrame(nl_frame, text="Natural Language Command", style='Custom.TFrame')
        command_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(command_frame, text="Enter command:", style='Heading.TLabel').pack(anchor='w', padx=5, pady=2)
        
        self.nl_command_var = tk.StringVar()
        command_entry = ttk.Entry(command_frame, textvariable=self.nl_command_var, width=80)
        command_entry.pack(fill='x', padx=5, pady=5)
        
        # Example commands
        examples_frame = ttk.LabelFrame(nl_frame, text="Example Commands", style='Custom.TFrame')
        examples_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        examples_text = scrolledtext.ScrolledText(examples_frame, height=10, width=80,
                                                 bg='#3d3d3d', fg='#ffffff', 
                                                 insertbackground='#ffffff')
        examples_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        examples = """💡 Example Natural Language Commands:

🔄 Format Conversion:
• "convert to mp3"
• "convert video.mp4 to wav"
• "change format to avi"

📏 Compression:
• "compress to 50MB"
• "reduce size by 50%"
• "compress video with high quality"

✂️ Trimming:
• "trim from 00:30 to 01:30"
• "extract 60 seconds starting at 01:00"
• "cut from 2 minutes to 5 minutes"

📐 Resizing/Cropping:
• "resize to 720x480"
• "crop to 500x500"
• "crop to 640x480 at position 100,100"

🎵 Audio:
• "extract audio from video"
• "get audio track"
• "remove noise from audio"
"""
        
        examples_text.insert('1.0', examples)
        examples_text.config(state='disabled')
        
        # Process button
        ttk.Button(nl_frame, text="🚀 Process Command", 
                  command=self.process_natural_language, style='Custom.TButton').pack(pady=10)
    
    def create_log_tab(self):
        """Create log/output tab"""
        log_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(log_frame, text="📋 Logs")
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=25, width=100,
                                                 bg='#1e1e1e', fg='#ffffff', 
                                                 insertbackground='#ffffff',
                                                 font=('Consolas', 10))
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clear log button
        ttk.Button(log_frame, text="🗑️ Clear Logs", 
                  command=self.clear_logs, style='Custom.TButton').pack(pady=10)
        
        # Initial log message
        self.log("🎬 Video/Audio Processing Toolkit initialized successfully!")
        self.log("📝 Ready to process your media files...")
    
    def select_files(self):
        """Select multiple files"""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
            ("Audio files", "*.mp3 *.wav *.flac *.aac *.ogg"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select media files",
            filetypes=filetypes
        )
        
        for file_path in files:
            if file_path not in self.uploaded_files:
                self.uploaded_files.append(file_path)
        
        self.refresh_file_tree()
        self.refresh_file_lists()
        self.log(f"📁 Selected {len(files)} file(s)")
    
    def select_folder(self):
        """Select all media files from a folder"""
        folder_path = filedialog.askdirectory(title="Select folder with media files")
        
        if folder_path:
            media_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', 
                              '.mp3', '.wav', '.flac', '.aac', '.ogg'}
            
            count = 0
            for file_path in Path(folder_path).rglob('*'):
                if file_path.suffix.lower() in media_extensions:
                    file_str = str(file_path)
                    if file_str not in self.uploaded_files:
                        self.uploaded_files.append(file_str)
                        count += 1
            
            self.refresh_file_tree()
            self.refresh_file_lists()
            self.log(f"📁 Added {count} media file(s) from folder")
    
    def clear_files(self):
        """Clear all uploaded files"""
        self.uploaded_files.clear()
        self.refresh_file_tree()
        self.refresh_file_lists()
        self.log("🗑️ Cleared all files")
    
    def refresh_file_tree(self):
        """Refresh the file tree display"""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add files
        for file_path in self.uploaded_files:
            path_obj = Path(file_path)
            name = path_obj.name
            
            try:
                size_mb = path_obj.stat().st_size / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"
            except:
                size_str = "Unknown"
            
            file_type = path_obj.suffix.upper()[1:] if path_obj.suffix else "Unknown"
            
            self.file_tree.insert('', 'end', values=(name, size_str, file_type))
    
    def refresh_file_lists(self):
        """Refresh all file combo boxes"""
        file_names = [Path(f).name for f in self.uploaded_files]
        
        self.conv_file_combo['values'] = file_names
        self.trim_file_combo['values'] = file_names
        self.ai_file_combo['values'] = file_names
        self.nl_file_combo['values'] = file_names
        
        # Set first file as default if available
        if file_names:
            if not self.conv_file_var.get():
                self.conv_file_var.set(file_names[0])
            if not self.trim_file_var.get():
                self.trim_file_var.set(file_names[0])
            if not self.ai_file_var.get():
                self.ai_file_var.set(file_names[0])
            if not self.nl_file_var.get():
                self.nl_file_var.set(file_names[0])
    
    def get_full_path(self, filename):
        """Get full path from filename"""
        for file_path in self.uploaded_files:
            if Path(file_path).name == filename:
                return file_path
        return None
    
    def start_conversion(self):
        """Start format conversion in a separate thread"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.conv_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file to convert!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._convert_file, args=(input_file,))
        thread.daemon = True
        thread.start()
    
    def _convert_file(self, input_file):
        """Convert file (runs in separate thread)"""
        self.processing = True
        self.update_status("🔄 Converting file...")
        self.progress_var.set(20)
        
        try:
            output_format = self.output_format_var.get()
            quality = self.quality_var.get()
            
            output_file = str(Path(input_file).with_suffix(f'.{output_format}'))
            base_name = Path(output_file).stem
            counter = 1
            
            # Avoid overwriting existing files
            while Path(output_file).exists():
                output_file = str(Path(input_file).parent / f"{base_name}_{counter}.{output_format}")
                counter += 1
            
            self.progress_var.set(40)
            
            # Build command based on format and quality
            if output_format in ['mp3', 'wav', 'flac']:
                quality_map = {'high': '320k', 'medium': '192k', 'low': '128k'}
                bitrate = quality_map.get(quality, '192k')
                command = f'ffmpeg -i "{input_file}" -b:a {bitrate} "{output_file}" -y'
            else:
                crf_map = {'high': '18', 'medium': '23', 'low': '28'}
                crf = crf_map.get(quality, '23')
                command = f'ffmpeg -i "{input_file}" -crf {crf} "{output_file}" -y'
            
            self.progress_var.set(60)
            
            # Add compression if enabled
            if self.compress_var.get() and output_format in ['mp4', 'avi', 'mov']:
                try:
                    target_mb = int(self.target_size_var.get())
                    duration = self._get_duration(input_file)
                    if duration > 0:
                        target_bitrate = int((target_mb * 8 * 1024) / duration * 0.9)
                        command = f'ffmpeg -i "{input_file}" -b:v {target_bitrate}k -maxrate {int(target_bitrate*1.2)}k "{output_file}" -y'
                except:
                    pass
            
            self.progress_var.set(80)
            self.log(f"🔧 Running: {command}")
            
            # Run conversion
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            self.progress_var.set(100)
            
            if result.returncode == 0:
                self.log(f"✅ Conversion successful! Output: {Path(output_file).name}")
                self.update_status("✅ Conversion completed successfully!")
                messagebox.showinfo("Success", f"File converted successfully!\nOutput: {Path(output_file).name}")
            else:
                self.log(f"❌ Conversion failed: {result.stderr}")
                self.update_status("❌ Conversion failed")
                messagebox.showerror("Error", f"Conversion failed!\n{result.stderr[:200]}...")
        
        except Exception as e:
            self.log(f"❌ Error during conversion: {str(e)}")
            self.update_status("❌ Conversion error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def start_trimming(self):
        """Start trimming/cropping in a separate thread"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.trim_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file to trim!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._trim_file, args=(input_file,))
        thread.daemon = True
        thread.start()
    
    def _trim_file(self, input_file):
        """Trim file (runs in separate thread)"""
        self.processing = True
        self.update_status("✂️ Trimming file...")
        self.progress_var.set(25)
        
        try:
            start_time = self.start_time_var.get()
            end_time = self.end_time_var.get()
            
            # Generate output filename
            suffix = Path(input_file).suffix
            output_file = str(Path(input_file).with_suffix(f'_trimmed{suffix}'))
            
            base_name = Path(output_file).stem
            counter = 1
            while Path(output_file).exists():
                output_file = str(Path(input_file).parent / f"{base_name}_{counter}{suffix}")
                counter += 1
            
            self.progress_var.set(50)
            
            # Build trim command
            command = f'ffmpeg -i "{input_file}" -ss {start_time} -to {end_time} -c copy "{output_file}" -y'
            
            # Add cropping if enabled
            if self.crop_var.get():
                try:
                    width = int(self.crop_width_var.get())
                    height = int(self.crop_height_var.get())
                    x = int(self.crop_x_var.get())
                    y = int(self.crop_y_var.get())
                    
                    command = f'ffmpeg -i "{input_file}" -ss {start_time} -to {end_time} -vf crop={width}:{height}:{x}:{y} "{output_file}" -y'
                except ValueError:
                    self.log("⚠️ Invalid crop dimensions, skipping cropping")
            
            self.progress_var.set(75)
            self.log(f"🔧 Running: {command}")
            
            # Run trimming
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            self.progress_var.set(100)
            
            if result.returncode == 0:
                self.log(f"✅ Trimming successful! Output: {Path(output_file).name}")
                self.update_status("✅ Trimming completed successfully!")
                messagebox.showinfo("Success", f"File trimmed successfully!\nOutput: {Path(output_file).name}")
            else:
                self.log(f"❌ Trimming failed: {result.stderr}")
                self.update_status("❌ Trimming failed")
                messagebox.showerror("Error", f"Trimming failed!\n{result.stderr[:200]}...")
        
        except Exception as e:
            self.log(f"❌ Error during trimming: {str(e)}")
            self.update_status("❌ Trimming error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def remove_noise(self):
        """Remove noise from audio"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.ai_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._remove_noise, args=(input_file,))
        thread.daemon = True
        thread.start()
    
    def _remove_noise(self, input_file):
        """Remove noise (runs in separate thread)"""
        self.processing = True
        self.update_status("🔇 Removing noise...")
        self.progress_var.set(20)
        
        try:
            output_file = str(Path(input_file).with_suffix('_denoised.wav'))
            
            base_name = Path(output_file).stem
            counter = 1
            while Path(output_file).exists():
                output_file = str(Path(input_file).parent / f"{base_name}_{counter}.wav")
                counter += 1
            
            self.progress_var.set(40)
            
            # Load audio
            self.log("📂 Loading audio file...")
            audio_data, sample_rate = librosa.load(input_file, sr=None)
            
            self.progress_var.set(60)
            
            # Remove noise
            self.log("🤖 Applying AI noise reduction...")
            denoised = nr.reduce_noise(y=audio_data, sr=sample_rate, stationary=False, prop_decrease=0.8)
            
            self.progress_var.set(80)
            
            # Save denoised audio
            self.log("💾 Saving denoised audio...")
            import scipy.io.wavfile as wav
            wav.write(output_file, sample_rate, (denoised * 32767).astype(np.int16))
            
            self.progress_var.set(100)
            
            self.log(f"✅ Noise removal successful! Output: {Path(output_file).name}")
            self.update_status("✅ Noise removal completed!")
            messagebox.showinfo("Success", f"Noise removed successfully!\nOutput: {Path(output_file).name}")
        
        except Exception as e:
            self.log(f"❌ Error during noise removal: {str(e)}")
            self.update_status("❌ Noise removal failed")
            messagebox.showerror("Error", f"Noise removal failed!\n{str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def generate_subtitles(self):
        """Generate subtitles using Whisper AI"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.ai_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._generate_subtitles, args=(input_file,))
        thread.daemon = True
        thread.start()
    
    def _generate_subtitles(self, input_file):
        """Generate subtitles (runs in separate thread)"""
        self.processing = True
        self.update_status("📝 Generating subtitles...")
        self.progress_var.set(10)
        
        try:
            language = self.subtitle_lang_var.get()
            output_file = str(Path(input_file).with_suffix('.srt'))
            
            base_name = Path(output_file).stem
            counter = 1
            while Path(output_file).exists():
                output_file = str(Path(input_file).parent / f"{base_name}_{counter}.srt")
                counter += 1
            
            self.progress_var.set(20)
            
            # Load Whisper model
            if self.whisper_model is None:
                self.log("🤖 Loading Whisper AI model...")
                self.whisper_model = whisper.load_model("base")
            
            self.progress_var.set(40)
            
            # Transcribe
            self.log(f"🎯 Transcribing audio (language: {language})...")
            result = self.whisper_model.transcribe(
                input_file, 
                language=None if language == 'auto' else language
            )
            
            self.progress_var.set(80)
            
            # Convert to SRT format
            self.log("💾 Converting to SRT format...")
            srt_content = self._convert_to_srt(result['segments'])
            
            # Save SRT file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            self.progress_var.set(100)
            
            self.log(f"✅ Subtitles generated! Output: {Path(output_file).name}")
            self.update_status("✅ Subtitles generated successfully!")
            messagebox.showinfo("Success", f"Subtitles generated successfully!\nOutput: {Path(output_file).name}")
        
        except Exception as e:
            self.log(f"❌ Error generating subtitles: {str(e)}")
            self.update_status("❌ Subtitle generation failed")
            messagebox.showerror("Error", f"Subtitle generation failed!\n{str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def smart_compress(self):
        """Smart video compression"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.ai_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._smart_compress, args=(input_file,))
        thread.daemon = True
        thread.start()
    
    def _smart_compress(self, input_file):
        """Smart compress (runs in separate thread)"""
        self.processing = True
        self.update_status("🧠 Smart compressing...")
        self.progress_var.set(25)
        
        try:
            quality = self.smart_quality_var.get()
            output_file = str(Path(input_file).with_suffix('_smart_compressed.mp4'))
            
            base_name = Path(output_file).stem
            counter = 1
            while Path(output_file).exists():
                output_file = str(Path(input_file).parent / f"{base_name}_{counter}.mp4")
                counter += 1
            
            self.progress_var.set(50)
            
            # Smart compression settings
            quality_settings = {
                'high': {'crf': '18', 'preset': 'slow'},
                'balanced': {'crf': '23', 'preset': 'medium'},
                'fast': {'crf': '28', 'preset': 'fast'}
            }
            
            settings = quality_settings[quality]
            command = f'ffmpeg -i "{input_file}" -crf {settings["crf"]} -preset {settings["preset"]} "{output_file}" -y'
            
            self.progress_var.set(75)
            self.log(f"🔧 Running: {command}")
            
            # Run compression
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            self.progress_var.set(100)
            
            if result.returncode == 0:
                self.log(f"✅ Smart compression successful! Output: {Path(output_file).name}")
                self.update_status("✅ Smart compression completed!")
                messagebox.showinfo("Success", f"Video compressed successfully!\nOutput: {Path(output_file).name}")
            else:
                self.log(f"❌ Compression failed: {result.stderr}")
                self.update_status("❌ Compression failed")
                messagebox.showerror("Error", f"Compression failed!\n{result.stderr[:200]}...")
        
        except Exception as e:
            self.log(f"❌ Error during compression: {str(e)}")
            self.update_status("❌ Compression error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def extract_audio(self):
        """Extract audio from video"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.ai_file_var.get()
        if not filename:
            messagebox.showerror("Error", "Please select a file!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._extract_audio, args=(input_file,))
        thread.daemon = True
        thread.start()
    
    def _extract_audio(self, input_file):
        """Extract audio (runs in separate thread)"""
        self.processing = True
        self.update_status("🎵 Extracting audio...")
        self.progress_var.set(30)
        
        try:
            output_file = str(Path(input_file).with_suffix('_audio.wav'))
            
            base_name = Path(output_file).stem
            counter = 1
            while Path(output_file).exists():
                output_file = str(Path(input_file).parent / f"{base_name}_{counter}.wav")
                counter += 1
            
            self.progress_var.set(60)
            
            command = f'ffmpeg -i "{input_file}" -vn -acodec pcm_s16le "{output_file}" -y'
            self.log(f"🔧 Running: {command}")
            
            # Run extraction
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            self.progress_var.set(100)
            
            if result.returncode == 0:
                self.log(f"✅ Audio extraction successful! Output: {Path(output_file).name}")
                self.update_status("✅ Audio extraction completed!")
                messagebox.showinfo("Success", f"Audio extracted successfully!\nOutput: {Path(output_file).name}")
            else:
                self.log(f"❌ Extraction failed: {result.stderr}")
                self.update_status("❌ Extraction failed")
                messagebox.showerror("Error", f"Audio extraction failed!\n{result.stderr[:200]}...")
        
        except Exception as e:
            self.log(f"❌ Error during extraction: {str(e)}")
            self.update_status("❌ Extraction error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def process_natural_language(self):
        """Process natural language command"""
        if self.processing:
            messagebox.showwarning("Processing", "Another operation is in progress!")
            return
        
        filename = self.nl_file_var.get()
        command = self.nl_command_var.get().strip()
        
        if not filename:
            messagebox.showerror("Error", "Please select a file!")
            return
        
        if not command:
            messagebox.showerror("Error", "Please enter a command!")
            return
        
        input_file = self.get_full_path(filename)
        if not input_file:
            messagebox.showerror("Error", "Selected file not found!")
            return
        
        # Start processing in thread
        thread = threading.Thread(target=self._process_nl_command, args=(input_file, command))
        thread.daemon = True
        thread.start()
    
    def _process_nl_command(self, input_file, command):
        """Process natural language command (runs in separate thread)"""
        self.processing = True
        self.update_status(f"💬 Processing: {command}")
        self.progress_var.set(20)
        
        try:
            command = command.lower().strip()
            self.log(f"💬 Processing command: '{command}'")
            
            # Parse command and generate output filename
            base_name = Path(input_file).stem
            
            self.progress_var.set(40)
            
            if "convert" in command and "mp3" in command:
                output_file = f"{base_name}_converted.mp3"
                ffmpeg_command = f'ffmpeg -i "{input_file}" -b:a 192k "{output_file}" -y'
            
            elif "compress" in command:
                if "mb" in command:
                    # Extract target size
                    import re
                    match = re.search(r'(\d+)\s*mb', command)
                    if match:
                        target_mb = int(match.group(1))
                        duration = self._get_duration(input_file)
                        if duration > 0:
                            target_bitrate = int((target_mb * 8 * 1024) / duration * 0.9)
                            output_file = f"{base_name}_compressed_{target_mb}mb.mp4"
                            ffmpeg_command = f'ffmpeg -i "{input_file}" -b:v {target_bitrate}k "{output_file}" -y'
                        else:
                            raise Exception("Could not determine video duration")
                    else:
                        output_file = f"{base_name}_compressed.mp4"
                        ffmpeg_command = f'ffmpeg -i "{input_file}" -crf 23 "{output_file}" -y'
                else:
                    output_file = f"{base_name}_compressed.mp4"
                    ffmpeg_command = f'ffmpeg -i "{input_file}" -crf 23 "{output_file}" -y'
            
            elif "trim" in command:
                # Extract time ranges
                time_pattern = r'(\d{1,2}:\d{2}(?::\d{2})?)'
                times = re.findall(time_pattern, command)
                if len(times) >= 2:
                    start_time, end_time = times[0], times[1]
                    output_file = f"{base_name}_trimmed{Path(input_file).suffix}"
                    ffmpeg_command = f'ffmpeg -i "{input_file}" -ss {start_time} -to {end_time} -c copy "{output_file}" -y'
                else:
                    raise Exception("Could not parse time range from command")
            
            elif "extract" in command and ("audio" in command or "sound" in command):
                output_file = f"{base_name}_audio.wav"
                ffmpeg_command = f'ffmpeg -i "{input_file}" -vn -acodec pcm_s16le "{output_file}" -y'
            
            elif "resize" in command:
                # Extract dimensions
                dim_pattern = r'(\d+)x(\d+)'
                match = re.search(dim_pattern, command)
                if match:
                    width, height = match.groups()
                    output_file = f"{base_name}_resized_{width}x{height}.mp4"
                    ffmpeg_command = f'ffmpeg -i "{input_file}" -vf scale={width}:{height} "{output_file}" -y'
                else:
                    raise Exception("Could not parse dimensions from command")
            
            elif "crop" in command:
                # Extract crop dimensions
                dim_pattern = r'(\d+)x(\d+)'
                match = re.search(dim_pattern, command)
                if match:
                    width, height = match.groups()
                    output_file = f"{base_name}_cropped_{width}x{height}.mp4"
                    ffmpeg_command = f'ffmpeg -i "{input_file}" -vf crop={width}:{height}:0:0 "{output_file}" -y'
                else:
                    raise Exception("Could not parse crop dimensions from command")
            
            else:
                raise Exception(f"Could not understand command: '{command}'")
            
            self.progress_var.set(60)
            
            # Make sure output file doesn't exist
            counter = 1
            original_output = output_file
            while Path(output_file).exists():
                base, ext = os.path.splitext(original_output)
                output_file = f"{base}_{counter}{ext}"
                counter += 1
            
            # Update command with final output filename
            ffmpeg_command = ffmpeg_command.replace(f'"{original_output}"', f'"{output_file}"')
            
            self.progress_var.set(80)
            self.log(f"🔧 Running: {ffmpeg_command}")
            
            # Execute command
            result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True)
            
            self.progress_var.set(100)
            
            if result.returncode == 0:
                self.log(f"✅ Command processed successfully! Output: {Path(output_file).name}")
                self.update_status("✅ Natural language command completed!")
                messagebox.showinfo("Success", f"Command processed successfully!\nOutput: {Path(output_file).name}")
            else:
                self.log(f"❌ Command failed: {result.stderr}")
                self.update_status("❌ Command failed")
                messagebox.showerror("Error", f"Command failed!\n{result.stderr[:200]}...")
        
        except Exception as e:
            self.log(f"❌ Error processing command: {str(e)}")
            self.update_status("❌ Command processing error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.processing = False
            self.progress_var.set(0)
    
    def _get_duration(self, input_file):
        """Get media duration in seconds"""
        cmd = f'ffprobe -v quiet -show_entries format=duration -of csv=p=0 "{input_file}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        try:
            return float(result.stdout.strip())
        except:
            return 0
    
    def _convert_to_srt(self, segments):
        """Convert Whisper segments to SRT format"""
        srt_content = ""
        for i, segment in enumerate(segments):
            start_time = self._seconds_to_srt_time(segment['start'])
            end_time = self._seconds_to_srt_time(segment['end'])
            text = segment['text'].strip()
            
            srt_content += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"
        
        return srt_content
    
    def _seconds_to_srt_time(self, seconds):
        """Convert seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_logs(self):
        """Clear log text"""
        self.log_text.delete(1.0, tk.END)
        self.log("📋 Logs cleared")
    
    def run(self):
        """Start the GUI application"""
        self.log("🚀 Video/Audio Processing Toolkit GUI started")
        self.log("📝 Select files and choose processing options from the tabs above")
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    # Check if FFmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found! Please install FFmpeg first:")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        exit(1)
    
    # Start GUI
    print("🚀 Starting Video/Audio Processing Toolkit GUI...")
    app = VideoAudioProcessorGUI()
    app.run()
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    return None

def extract_transcript():
    url = url_entry.get()
    video_id = get_video_id(url)
    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube URL.")
        return
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # ✅ Works if package is correct
        text_area.delete(1.0, tk.END)
        for entry in transcript:
            timestamp = f"[{int(entry['start']//60):02d}:{int(entry['start']%60):02d}]"
            text_area.insert(tk.END, f"{timestamp} {entry['text']}\n\n", "timestamp")
        messagebox.showinfo("Success", "Transcript Extracted!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not extract transcript.\n{e}")

def save_transcript():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        content = text_area.get(1.0, tk.END)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", "Transcript saved successfully!")

def apply_tag(tag):
    try:
        start, end = text_area.index(tk.SEL_FIRST), text_area.index(tk.SEL_LAST)
        text_area.tag_add(tag, start, end)
    except:
        messagebox.showwarning("Warning", "Please select text first!")

def remove_tags():
    try:
        start, end = text_area.index(tk.SEL_FIRST), text_area.index(tk.SEL_LAST)
        for tag in ["bold", "underline", "highlight"]:
            text_area.tag_remove(tag, start, end)
    except:
        messagebox.showwarning("Warning", "Please select text first!")

root = tk.Tk()
root.title("YouTube Transcript Extractor")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="YouTube Video URL:").pack(side=tk.LEFT)
url_entry = tk.Entry(frame, width=60)
url_entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Extract", command=extract_transcript).pack(side=tk.LEFT)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 12))
text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

text_area.tag_configure("timestamp", foreground="blue", font=("Segoe UI", 12, "bold"))
text_area.tag_configure("bold", font=("Segoe UI", 12, "bold"))
text_area.tag_configure("underline", underline=True)
text_area.tag_configure("highlight", background="yellow")

toolbar = tk.Frame(root)
toolbar.pack(pady=5)
tk.Button(toolbar, text="Bold", command=lambda: apply_tag("bold")).pack(side=tk.LEFT, padx=3)
tk.Button(toolbar, text="Underline", command=lambda: apply_tag("underline")).pack(side=tk.LEFT, padx=3)
tk.Button(toolbar, text="Highlight", command=lambda: apply_tag("highlight")).pack(side=tk.LEFT, padx=3)
tk.Button(toolbar, text="Unhighlight", command=remove_tags).pack(side=tk.LEFT, padx=3)
tk.Button(toolbar, text="Save", command=save_transcript).pack(side=tk.RIGHT, padx=3)

root.mainloop()

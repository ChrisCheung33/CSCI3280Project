import tkinter as tk
import network

class MusicSearchGUI:
    def __init__(self, network):
        self.network = network
        self.window = tk.Tk()
        self.window.title("Music Search")
        self.query_var = tk.StringVar()
        self.query_entry = tk.Entry(self.window, textvariable=self.query_var)
        self.query_entry.pack()
        self.search_button = tk.Button(self.window, text="Search", command=self.search)
        self.search_button.pack()
        self.results_listbox = tk.Listbox(self.window)
        self.results_listbox.pack()

    def search(self):
        query = self.query_var.get()
        results = set()
        ip_addresses = self.network.get_ip_addresses()
        for ip in ip_addresses:
            results.update(self.network.client(ip, query))
        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, result)

    def run(self):
        self.window.mainloop()

network = network.network
gui = MusicSearchGUI(network)
gui.run()
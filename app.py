import traceback
import sys

try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import simpledialog
    import main
    import mysql.connector
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    def img_path(filename): return os.path.join(BASE_DIR, filename)
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="root")
        cursor = connection.cursor()
        main.initialize_db(cursor, connection)
    except mysql.connector.Error as err:
        temp_root = Tk()
        temp_root.withdraw()
        messagebox.showerror("Database Offline", f"Could not connect to MySQL.\nMake sure XAMPP/MySQL is running.\n\nError: {err}")
        temp_root.destroy()
        sys.exit()

    root = Tk()
    root.title('Library Connect')
    root.geometry('950x500+300+200')
    root.configure(bg='#fff')
    root.resizable(False, False)

    page = 1

    def bind_placeholder(entry, text, is_password=False):
        entry.insert(0, text)
        entry.config(fg='gray')
        if is_password: entry.config(show='')

        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, 'end')
                entry.config(fg='black')
                if is_password: entry.config(show='*')

        def on_focus_out(e):
            if entry.get() == '':
                entry.insert(0, text)
                entry.config(fg='gray')
                if is_password: entry.config(show='')

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def reset_input(entry, text, is_password=False):
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.config(fg='gray')
        if is_password: entry.config(show='')

    def toggle_password(entry, btn, placeholder):
        if entry.get() == placeholder: return
        if entry.cget('show') == '*':
            entry.config(show='')
            btn.config(text='Hide')
        else:
            entry.config(show='*')
            btn.config(text='👁')

    # ── FORCED PASSWORD CHANGE ───────────────────────────────────────────────────
    def force_password_change(username, role):
        change_win = Toplevel(root)
        change_win.title("Mandatory Password Update")
        change_win.geometry('400x350+400+300')
        change_win.configure(bg='#fff')
        change_win.grab_set() 

        Label(change_win, text="Reset Complete!", font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#fff', fg='#652d90').place(x=90, y=20)
        Label(change_win, text="Please set a new password to continue.", bg='#fff', fg='gray').place(x=85, y=60)

        new_pass = Entry(change_win, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
        new_pass.place(x=50, y=120)
        bind_placeholder(new_pass, 'New Password', True)
        Frame(change_win, width=295, height=2, bg='black').place(x=45, y=147)
        
        btn_eye1 = Button(change_win, text="👁", bd=0, bg='white', cursor='hand2', command=lambda: toggle_password(new_pass, btn_eye1, 'New Password'))
        btn_eye1.place(x=310, y=120)

        confirm_pass = Entry(change_win, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
        confirm_pass.place(x=50, y=190)
        bind_placeholder(confirm_pass, 'Confirm Password', True)
        Frame(change_win, width=295, height=2, bg='black').place(x=45, y=217)
        
        btn_eye2 = Button(change_win, text="👁", bd=0, bg='white', cursor='hand2', command=lambda: toggle_password(confirm_pass, btn_eye2, 'Confirm Password'))
        btn_eye2.place(x=310, y=190)

        def save_new_password():
            p1 = new_pass.get().strip()
            p2 = confirm_pass.get().strip()
            
            if p1 == 'New Password' or p2 == 'Confirm Password':
                messagebox.showerror("Error", "Please fill all fields.", parent=change_win)
                return
            if len(p1) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters.", parent=change_win)
                return
            if p1 != p2:
                messagebox.showerror("Error", "Passwords do not match!", parent=change_win)
                return
            
            main.dbupdatepassword(cursor, username, p1)
            connection.commit()
            messagebox.showinfo("Success", "Password updated successfully!", parent=change_win)
            change_win.destroy()
            
            if role == 'admin': open_admin()
            else: open_user_dashboard(username)

        Button(change_win, width=25, pady=7, text='Save Password', bg='#652d90', fg='white', border=0, command=save_new_password).place(x=100, y=260)

    def open_admin():
        admin_screen = Toplevel(root)
        admin_screen.title("Admin Controls")
        admin_screen.geometry("800x500")
        admin_screen.configure(bg='#fff')
        
        Label(admin_screen, text="Admin Dashboard", font=('Microsoft Yahei UI Light', 23, 'bold'), bg='#fff', fg='#652d90').pack(pady=15)
        list_frame = Frame(admin_screen, bg='#fff')
        list_frame.pack(fill=BOTH, expand=True, padx=20)
        
        def refresh_admin():
            for widget in list_frame.winfo_children(): widget.destroy()
            users = main.get_all_users(cursor)
            
            Label(list_frame, text="Username".ljust(20) + "Joined".ljust(15) + "Rank".ljust(10) + "Reset?", font=('Courier New', 12, 'bold'), bg='#fff').pack(anchor="w")
            for u in users:
                row = Frame(list_frame, bg='#f7f7f7', pady=5)
                row.pack(fill=X, pady=2)
                
                rank = main.get_user_rank(cursor, u[0])
                rank_str = f"#{rank}" if rank > 0 else "N/A"
                info_text = f"{u[0][:15].ljust(20)}{str(u[1]).ljust(15)}{rank_str.ljust(10)}{'YES' if u[2] else 'NO'}"
                
                Label(row, text=info_text, font=('Courier New', 11), bg='#f7f7f7').pack(side=LEFT)
                if u[2]:
                    Button(row, text="Accept Reset", bg="orange", border=0, command=lambda un=u[0]: handle_reset(un)).pack(side=LEFT, padx=10)
                Button(row, text="Del", bg="red", fg="white", border=0, width=5, command=lambda un=u[0]: handle_delete(un)).pack(side=RIGHT, padx=10)

        def handle_reset(uname):
            main.approve_reset(cursor, uname)
            connection.commit()
            messagebox.showinfo("Reset", f"{uname}'s password is now '{uname}@123'")
            refresh_admin()

        def handle_delete(uname):
            if messagebox.askyesno("Confirm", f"Delete {uname}?"):
                main.delete_user(cursor, uname)
                connection.commit()
                refresh_admin()

        def logout_admin():
            admin_screen.destroy()
            reset_input(user, 'Username')
            reset_input(code, 'Password', True)
            root.deiconify()

        Button(admin_screen, text="Logout", bg="#652d90", fg="white", width=15, command=logout_admin).pack(pady=20)
        refresh_admin()

    def open_user_dashboard(username):
        global page
        page = 1
        watchlist = Toplevel(root)
        watchlist.geometry("950x500")
        watchlist.configure(bg="#ffffff")

        frame = Frame(watchlist, bg="#ffffff")
        frame.place(x=0, y=0, width=950, height=500)

        bg_img = PhotoImage(file=img_path("background1.png"))
        bg_lbl = Label(frame, image=bg_img, bg="#ffffff")
        bg_lbl.image = bg_img
        bg_lbl.pack()

        rank_num = main.get_user_rank(cursor, username)
        rank_img = None
        rank_title = ""
        if rank_num == 1: 
            rank_img = PhotoImage(file=img_path("gold.png"))
            rank_title = "🥇 GOLD (Rank #1)"
        elif rank_num == 2: 
            rank_img = PhotoImage(file=img_path("silver.png"))
            rank_title = "🥈 SILVER (Rank #2)"
        elif rank_num == 3: 
            rank_img = PhotoImage(file=img_path("bronze.png"))
            rank_title = "🥉 BRONZE (Rank #3)"

        if rank_img:
            r_lbl = Label(frame, image=rank_img, bg="#ffffff")
            r_lbl.image = rank_img
            r_lbl.place(x=736, y=140)
            Label(frame, text=rank_title, font=('Arial', 14, 'bold'), fg='#652d90', bg='#ffffff').place(x=710, y=300)
        else:
            rank_text = "Not Ranked" if rank_num == 0 else f"Rank #{rank_num}"
            Label(frame, text=rank_text, font=('Arial', 24, 'bold'), fg='#652d90', bg='#ffffff').place(x=750, y=220)

        def add():
            watchlist.withdraw()
            screen = Toplevel(root)
            screen.title("Add Book")
            screen.geometry('950x500')
            screen.configure(bg='#fff')

            screen.img = PhotoImage(file=img_path('Login.png'))
            Label(screen, image=screen.img, bg='#fff').place(x=50, y=140)
            f1 = Frame(screen, width=350, height=350, bg="white")
            f1.place(x=488, y=78)
            Label(f1, text='Add book', fg='#652d90', bg='#fff', font=('Microsoft Yahei UI Light', 23, 'bold')).place(x=100, y=5)

            book_ent = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
            book_ent.place(x=30, y=60)
            bind_placeholder(book_ent, 'Book Title')
            Frame(f1, width=295, height=2, bg='black').place(x=25, y=85)

            auth_ent = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
            auth_ent.place(x=30, y=110)
            bind_placeholder(auth_ent, 'Author')
            Frame(f1, width=295, height=2, bg='black').place(x=25, y=135)

            max_ent = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
            max_ent.place(x=30, y=160)
            bind_placeholder(max_ent, 'Total Chapters')
            Frame(f1, width=295, height=2, bg='black').place(x=25, y=185)

            read_ent = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
            read_ent.place(x=30, y=210)
            bind_placeholder(read_ent, 'Chapters Read')
            Frame(f1, width=295, height=2, bg='black').place(x=25, y=235)

            Label(f1, text="Rating:", bg='#fff', fg='gray').place(x=30, y=250)
            rating_var = StringVar(value="3 ★★★")
            OptionMenu(f1, rating_var, *["1 ★", "2 ★★", "3 ★★★", "4 ★★★★", "5 ★★★★★"]).place(x=100, y=245)

            def addbook():
                t, a, c, r = book_ent.get().strip(), auth_ent.get().strip(), max_ent.get().strip(), read_ent.get().strip()
                if t == 'Book Title' or a == 'Author':
                    messagebox.showerror("Error", "Fields cannot be empty!")
                    return
                if not c.isdigit() or not r.isdigit():
                    messagebox.showerror("Error", "Chapters must be numbers!")
                    return
                if int(r) > int(c):
                    messagebox.showerror("Error", "Read chapters cannot exceed total!")
                    return
                    
                try:
                    main.dbaddbook(cursor, username, t, a, int(c), int(r), int(rating_var.get()[0]))
                    connection.commit()
                    screen.destroy()
                    watchlist.deiconify()
                    refresh_rows(frame, main.dbview(cursor, username), page)
                except mysql.connector.errors.IntegrityError:
                    messagebox.showerror("Error", "Book already exists!")

            Button(f1, width=15, pady=7, text='Add book', bg='#652d90', fg='white', border=0, command=addbook).place(x=35, y=300)
            Button(f1, width=15, pady=7, text='Cancel', bg='gray', fg='white', border=0, command=lambda: [screen.destroy(), watchlist.deiconify()]).place(x=175, y=300)

        img0 = PhotoImage(file=img_path("img0.png"))
        btn_add = Button(frame, image=img0, borderwidth=0, command=add, bg="#ffffff")
        btn_add.image = img0
        btn_add.place(x=650, y=430, width=47, height=56)

        def logout_user():
            watchlist.destroy()
            reset_input(user, 'Username')
            reset_input(code, 'Password', True)
            root.deiconify()

        img3 = PhotoImage(file=img_path("img3.png"))
        btn_out = Button(frame, image=img3, borderwidth=0, command=logout_user, bg="#ffffff")
        btn_out.image = img3
        btn_out.place(x=870, y=20, width=35, height=32)

        rect = Frame(frame, bg="#F7F7F7")
        rect.place(x=20, y=75, width=670, height=20)
        Label(rect, text="BookName".ljust(20) + "Progress".ljust(15) + "Rating".ljust(15), fg='#652d90', bg='#F7F7F7', font=('Courier New', 13, 'bold')).pack(side="left")

        def update_ch(b_name, max_c):
            val = simpledialog.askinteger("Update", f"Chapters read? (Max {max_c})")
            if val is not None and 0 <= val <= max_c:
                main.dbupdateprogress(cursor, username, b_name, val)
                connection.commit()
                refresh_rows(frame, main.dbview(cursor, username), page)

        def delete_bk(b_name):
            if messagebox.askyesno("Confirm", f"Delete {b_name}?"):
                main.dbdeletebook(cursor, username, b_name)
                connection.commit()
                refresh_rows(frame, main.dbview(cursor, username), page)

        def refresh_rows(tgt_frame, book_list, pg):
            for c in tgt_frame.winfo_children():
                if isinstance(c, Frame) and c.winfo_y() in [95, 155, 220, 290, 365]: c.destroy()
            
            start, end = (pg * 5) - 4, pg * 5
            upper = end if end <= len(book_list) else len(book_list)
            positions = [95, 155, 220, 290, 365]
            
            for idx, i in enumerate(range(start - 1, upper)):
                b = book_list[i]
                rf = Frame(tgt_frame, bg="#F7F7F7")
                rf.place(x=20, y=positions[idx], width=670, height=40)
                text = str(b[1][:15]).ljust(20) + f"{b[3]}/{b[2]}".ljust(15) + ("★" * b[4]).ljust(15)
                Label(rf, text=text, fg='#652d90', bg='#F7F7F7', font=('Courier New', 13, 'bold')).pack(side="left")
                Button(rf, text="Del", fg="red", border=1, command=lambda n=b[1]: delete_bk(n)).pack(side="right", padx=5)
                Button(rf, text="Update", border=1, command=lambda n=b[1], m=b[2]: update_ch(n, m)).pack(side="right", padx=5)

        def forward():
            global page
            if (page * 5) < len(main.dbview(cursor, username)):
                page += 1
                refresh_rows(frame, main.dbview(cursor, username), page)

        def backward():
            global page
            if page > 1:
                page -= 1
                refresh_rows(frame, main.dbview(cursor, username), page)

        img1 = PhotoImage(file=img_path("img1.png"))
        btn_fwd = Button(frame, image=img1, borderwidth=0, command=forward, bg="#ffffff")
        btn_fwd.image = img1
        btn_fwd.place(x=376, y=440, width=61, height=37)

        img2 = PhotoImage(file=img_path("img2.png"))
        btn_bwd = Button(frame, image=img2, borderwidth=0, command=backward, bg="#ffffff")
        btn_bwd.image = img2
        btn_bwd.place(x=314, y=440, width=61, height=37)

        refresh_rows(frame, main.dbview(cursor, username), page)
        Label(frame, text=username, fg='black', bg='#3D708D', font=('JosefinSansRoman-Regular', 14, 'bold')).place(x=800, y=20)

    def signin():
        uname = user.get().strip()
        pwd = code.get().strip()
        
        success, role = main.dbsignin(cursor, uname, pwd)
        if success:
            root.withdraw()
            if pwd == f"{uname}@123":
                force_password_change(uname, role)
            else:
                if role == 'admin': open_admin()
                else: open_user_dashboard(uname)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup():
        root.withdraw()
        screen = Toplevel(root)
        screen.title("Signup")
        screen.geometry('950x500+300+200')
        screen.configure(bg='#fff')
        screen.resizable(False, False)

        screen.img = PhotoImage(file=img_path('Login.png'))
        Label(screen, image=screen.img, bg='#fff').place(x=50, y=140)

        f1 = Frame(screen, width=350, height=350, bg="white")
        f1.place(x=488, y=78)

        Label(f1, text='Sign up', fg='#652d90', bg='#fff', font=('Microsoft Yahei UI Light', 23, 'bold')).place(x=100, y=5)

        user_su = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
        user_su.place(x=30, y=80)
        bind_placeholder(user_su, 'Username')
        Frame(f1, width=295, height=2, bg='black').place(x=25, y=107)

        code_su = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
        code_su.place(x=30, y=140)
        bind_placeholder(code_su, 'Password', True)
        Frame(f1, width=295, height=2, bg='black').place(x=25, y=167)
        
        btn_eye1 = Button(f1, text="👁", bd=0, bg='white', cursor='hand2', command=lambda: toggle_password(code_su, btn_eye1, 'Password'))
        btn_eye1.place(x=290, y=140)

        confirm_su = Entry(f1, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
        confirm_su.place(x=30, y=200)
        bind_placeholder(confirm_su, 'Confirm Password', True)
        Frame(f1, width=295, height=2, bg='black').place(x=25, y=227)
        
        btn_eye2 = Button(f1, text="👁", bd=0, bg='white', cursor='hand2', command=lambda: toggle_password(confirm_su, btn_eye2, 'Confirm Password'))
        btn_eye2.place(x=290, y=200)

        def newdetails():
            n, p, cp = user_su.get().strip(), code_su.get().strip(), confirm_su.get().strip()
            if n == 'Username' or p == 'Password':
                messagebox.showerror("Error", "Please fill all fields.")
                return
            if len(p) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters.")
                return
            if p != cp:
                messagebox.showerror("Error", "Passwords do not match")
                return
            try:
                main.dbsignup(cursor, n, p)
                connection.commit()
                messagebox.showinfo("Success", "Account created! Please sign in.")
                screen.destroy()
                root.deiconify()
            except mysql.connector.errors.IntegrityError:
                messagebox.showerror("Invalid", "Username already exists")

        def go_back():
            screen.destroy()
            reset_input(user, 'Username')
            reset_input(code, 'Password', True)
            root.deiconify()

        Button(f1, width=39, pady=7, text='Sign up', bg='#652d90', fg='white', border=0, command=newdetails).place(x=35, y=260)
        Button(f1, text='< Back to Login', border=0, bg='white', cursor='hand2', fg='gray', command=go_back).place(x=130, y=305)

    try:
        img = PhotoImage(file=img_path('Login.png'))
        Label(root, image=img, bg='#fff').place(x=50, y=140)
    except TclError as e:
        messagebox.showwarning("Missing Image", f"Could not load Login.png.\nError: {e}")

    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=488, y=78)

    Label(frame, text='Sign in', fg='#652d90', bg='#fff', font=('Microsoft Yahei UI Light', 23, 'bold')).place(x=100, y=5)

    user = Entry(frame, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
    user.place(x=30, y=80)
    bind_placeholder(user, 'Username')
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    code = Entry(frame, width=28, fg='black', border=0, bg='#fff', font=('Microsoft Yahei UI Light', 12))
    code.place(x=30, y=150)
    bind_placeholder(code, 'Password', True)
    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    eye_btn = Button(frame, text="👁", bd=0, bg='white', cursor='hand2', command=lambda: toggle_password(code, eye_btn, 'Password'))
    eye_btn.place(x=290, y=148)

    Button(frame, width=39, pady=7, text='Sign in', bg='#652d90', fg='white', border=0, command=signin).place(x=35, y=204)
    Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft Yahei UI Light', 9)).place(x=75, y=270)
    Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#652d90', command=signup).place(x=215, y=270)

    def forgot_password():
        uname = simpledialog.askstring("Reset", "Enter your username to request reset:")
        if uname:
            main.request_password_reset(cursor, uname)
            connection.commit()
            messagebox.showinfo("Request Sent", f"Reset request sent to admin.\nOnce approved, your temporary password will be:\n\n{uname}@123")

    Button(frame, text='Forgot Password?', bd=0, bg='white', fg='blue', cursor='hand2', command=forgot_password).place(x=120, y=240)

    root.protocol("WM_DELETE_WINDOW", lambda: [cursor.close(), connection.close(), root.destroy()])
    root.mainloop()

except Exception as e:
    temp_root = Tk()
    temp_root.withdraw()
    messagebox.showerror("Fatal Error", f"The application crashed:\n\n{str(e)}\n\nCheck your console for the full traceback.")
    traceback.print_exc()
    temp_root.destroy()
    sys.exit()

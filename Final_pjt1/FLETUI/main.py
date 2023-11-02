import flet as ft

def main(page:ft.Page):
    page.title = 'Hello UI'

    def on_click_handler(e):
        print('Button Accept', text_field.value)
        page.add(ft.Text(text_field.value))
        text_field.value = ''
        page.update()

    page.add(ft.Text('빅데이터 4기 first-line 조'))

    text_field = ft.TextField(hint_text='이름을 입력하세요', on_submit=on_click_handler)
    page.add(text_field)

    page.add(ft.ElevatedButton('Send', on_click=on_click_handler))



    page.update()    

ft.app(target=main)
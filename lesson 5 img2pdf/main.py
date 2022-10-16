import requests
import img2pdf


def get_data():
    for i in range(1, 49):
        url = f'https://recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        req = requests.get(url=url, headers=headers)

        with open(f'images/{i}.jpg', 'wb') as file:
            file.write(req.content)

def create_pdf():
    images_list = []
    for i in range(1, 49):
        images_list.append(f'images/{i}.jpg')
    with open('result.pdf', 'wb') as file:
        file.write(img2pdf.convert(images_list))

if __name__ == '__main__':
    # get_data()
    create_pdf()


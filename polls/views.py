from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

from polls.models import Gifts, Board, Ship, BoardAccess, GiftWinners, MyShots, Image, MyResults
from polls.forms import GiftForm, BoardForm, ShipForm, ShotForm, BattleForm, ImageForm
from django.contrib.auth.models import User


def index_page(request):
    context = {}
    context['authors'] = 'Anton and Stanislav'
    context['pages'] = 2

    return render(request, 'index.html', context)


def SeaBattle_page(request):
    context = {}
    errors = []
    if not request.user.is_authenticated:
        errors.append('Для дальнейших действий зарегестрируйтесь')
    if len(errors) > 0:
        context['errors'] = errors
    boards = Board.objects.all()
    game_boards = []
    for board in boards:
        if request.user.id in board.users_id:
            game_boards.append(board)
    context['boards'] = game_boards
    return render(request, 'user/SeaBattle.html', context)


def mygift_page(request):
    context = {}
    errors = []
    if not request.user.is_authenticated:
        errors.append('Для дальнейших действий зарегестрируйтесь')
    if len(errors) > 0:
        context['errors'] = errors
    gifts = Gifts.objects.all()
    gifts_winn = GiftWinners.objects.all()
    my_gifts = []

    for gift in gifts_winn:
        if gift.winner_id == request.user.id:
            for gi in gifts:
                if gi.id == gift.gift_id:
                    my_gifts.append(gi)
    context['my_gifts'] = my_gifts

    return render(request, 'user/MyGifts.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def check_admin(request):
    return request.user.is_superuser


@staff_member_required
def delete_field(request, board_id):
    context = {}
    ships = Ship.objects.all()
    board = Board.objects.get(id=board_id)
    acc = BoardAccess.objects.all()
    is_not_playing = True
    errors = []
    for access in acc:
        if access.board_id == board_id:
            if access.start_shot != access.shots:
                is_not_playing = False
    if not is_not_playing:
        errors.append('На данном поле некоторые игроки начали битву, пока они не доиграют вы не можете его удалить')
        context['errors'] = errors
    if is_not_playing:
        for access in acc:
            if access.board_id == board_id:
                access.delete()
        for ship in ships:
            if ship.board_id == board_id:
                ship.delete()
        board.delete()

    return render(request, 'admin/fields.html', context)


@staff_member_required
def delete_user_and_shots(request, access_id):
    context = {}
    is_not_playing = True
    errors = []
    acc = BoardAccess.objects.all()
    for access in acc:
        if access.id == access_id:
            if access.start_shot != access.shots:
                is_not_playing = False
    if not is_not_playing:
        errors.append('На данном поле некоторые игроки начали битву, пока они не доиграют вы не можете удалять этих пользователей')
        context['errors'] = errors
    if is_not_playing:
        for access in acc:
            if access.id == access_id:
                access.delete()
    return render(request, 'admin/addshot.html', context)


@staff_member_required
def delete_gift(request, gift_id):
    context = {}
    gift = Gifts.objects.get(id=gift_id)
    ships = Ship.objects.all()
    for ship in ships:
        if ship.gift_id == gift_id:
            ship.delete()
    gift.delete()
    return render(request, 'admin/settings_gift.html', context)


@staff_member_required
def delete_ship(request, ship_id):
    context = {}
    ship = Ship.objects.get(id=ship_id)
    ship.delete()
    return render(request, 'admin/AddShip.html', context)


@staff_member_required
def fields(request):
    context = {}
    context['boards'] = Board.objects.all()
    return render(request, 'admin/fields.html', context)


def add_ship(request, board_id):
    context = {}
    errors = []
    gifts = Gifts.objects.all()
    context['gifts'] = gifts
    ships = Ship.objects.filter(board_id=board_id)
    context['ships'] = ships
    board = Board.objects.get(id=board_id)
    context['board'] = board
    acc = BoardAccess.objects.all()
    is_not_playing = True
    for access in acc:
        if access.board_id == board_id:
            if access.start_shot != access.shots:
                is_not_playing = False
    if not is_not_playing:
        errors.append('На данном поле некоторые игроки начали битву, пока они не доиграют вы не можете удалять этих пользователей ')

    if request.method == "POST":
        form = ShipForm(request.POST)
        if form.is_valid():
            x = form.cleaned_data['x']
            y = form.cleaned_data['y']
            gift_id = form.cleaned_data['gift_id']
            is_exists = False
            for gift in gifts:
                if gift.id == gift_id:
                    is_exists = True
            if not is_exists:
                errors.append('Неправильный id, данного приза не существует')
            for ship in ships:
                if ship.x == x and ship.y == y:
                    errors.append('Корабль с данными координатами уже существует на данном поле, пожалуйста введите другие координаты')
            if len(errors) > 0:
                context['errors'] = errors
            else:
                record = Ship(x=x, y=y, board_id=board_id, gift_id=gift_id)
                record.save()
    return render(request, 'admin/AddShip.html', context)


@staff_member_required
def create_board(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    description = '''
                web-игра морской бой. За каждую
                покупку на определенную сумму, будут начисляться бонусные
                выстрелы. Эти выстрелы можно тратить на поле морского боя и,
                если вы попадете в корабль, то получаете какой-либо гарантированный приз.
                '''
    context['description'] = description
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            record = Board(name=name, size=size, users_id=[])
            record.save()
        else:
            print('aaaaaa')
    return render(request, 'admin/create_board.html', context)


@staff_member_required
def users_page(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    return render(request, 'admin/users.html', context)


@staff_member_required
def edit_fields(request, board_id):
    context = {}
    all_users = User.objects.all()
    context['users'] = all_users
    description = '''
                    web-игра морской бой. За каждую
                    покупку на определенную сумму, будут начисляться бонусные
                    выстрелы. Эти выстрелы можно тратить на поле морского боя и,
                    если вы попадете в корабль, то получаете какой-либо гарантированный приз.
                    '''
    context['description'] = description
    board = Board.objects.get(id=board_id)
    context['board'] = board
    array_users = []
    errors = []
    acc = BoardAccess.objects.all()
    for user in all_users:
        if user.id in board.users_id:
            array_users.append(user)
    context['array_users'] = array_users
    is_not_playing = True
    for access in acc:
        if access.board_id == board_id:
            if access.start_shot != access.shots:
                is_not_playing = False
    if not is_not_playing:
        errors.append('На данном поле некоторые игроки начали битву, пока они не доиграют вы не можете удалять этих пользователей ')
    if len(errors) == 0:
        if request.method == "POST":
            form = BoardForm(request.POST)
            if form.is_valid():
                board.name = form.cleaned_data['name']
                board.size = form.cleaned_data['size']
                board.save()
    else:
        context['errors'] = errors
    return render(request, 'admin/edit_fields.html', context)


@staff_member_required
def settings_gift(request):
    context = {}
    im = Image.objects.all()
    context['image'] = im
    arr_im = []
    gifts = Gifts.objects.all()
    images_array = []
    g_id = []
    for img in im:
        images_array.append(img.gift_id)
    for gift in gifts:
        g_id.append(gift.id)
        if not(gift.id in images_array):
            record = Image(gift_id=gift.id)
            record.save()
    for image in im:
        if arr_im.count(image.gift_id) == 0:
            arr_im.append(image.gift_id)
        else:
            image.delete()
        if not(image.gift_id in g_id):
            image.delete()
    context['history'] = Gifts.objects.all()
    return render(request, 'admin/settings_gift.html', context)


@staff_member_required
def create_gift(request):
    context = {}
    gifts = Gifts.objects.all()
    images = Image.objects.all()
    images_array = []
    for img in images:
        images_array.append(img.gift_id)
    errors = []
    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            for gift in gifts:
                if gift.name == name:
                    errors.append('Приз с данным названием уже существует, пожалуйста введите другое название')
            if len(errors) > 0:
                context['errors'] = errors
            else:
                record = Gifts(name=name, description=description)
                record.save()

    return render(request, 'admin/Creategift.html', context)


def add_image(request, gift_id):
    images = Image.objects.all()
    context = {}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            img = form.cleaned_data['Img']
            for im in images:
                if im.gift_id == gift_id:
                    im.delete()
            image = Image(gift_id=gift_id, Img=img)
            image.save()
            messages.success(request, 'Фотография приза изменена.')
            return HttpResponseRedirect("/settingsgift/")

    else:
        form = ImageForm()
        context['form'] = form

    return render(request, 'admin/addimage.html', context)


def battle_page(request, board_id):
    context = {}
    acc = BoardAccess.objects.all()
    for access in acc:
        if access.board_id == board_id:
            acc_obj = access
            break
    context['access'] = acc_obj
    recent_sh = MyShots.objects.all()
    recent_shots = []
    for rec in recent_sh:
        if rec.user_id == request.user.id and rec.board_id == board_id:
            recent_shots.append(rec)
    description = '''
                web-игра морской бой. За каждую\n
                покупку на определенную сумму, будут начисляться бонусные\n
                выстрелы. Эти выстрелы можно тратить на поле морского боя и,\n
                если вы попадете в корабль, то получаете какой-либо гарантированный приз.
                Совершайте выстрелы и выигрывайте призы, только учтите, что выстрелы ограничены
                '''
    context['description'] = description
    board = Board.objects.get(id=board_id)
    ships = Ship.objects.filter(board_id=board_id)
    gifts = Gifts.objects.all()
    field = [''] * board.size * board.size
    context['field'] = field
    context['board'] = board
    errors = []
    my_res = MyResults.objects.all()
    if request.user.is_superuser:
        errors.append('Админы не могут играть')
    if request.method == "POST":
        form = BattleForm(request.POST)
        if form.is_valid():
            x = form.cleaned_data['x']
            y = form.cleaned_data['y']
            for shot in recent_shots:
                if shot.x == x and shot.y == y:
                    errors.append('Вы уже совершали выстрел в данную точку')
            if len(errors) == 0:
                rec = MyShots(x=x, y=y, user_id=request.user.id, board_id=board_id)
                rec.save()
                acc_obj.shots = acc_obj.shots - 1
                acc_obj.save()
                is_win = False
                win = []
                is_first_hit = True
                for ship in ships:
                    if ship.x == x and ship.y == y:
                        is_win = True
                        for gift in gifts:
                            if gift.id == ship.gift_id:
                                win.append(gift)
                                for res in my_res:
                                    if res.board_id == board_id and res.user == request.user.id:
                                        is_first_hit = False
                                        res.gifts_id.append(gift.id)
                                        res.save()
                                if is_first_hit:
                                    my_gifts = []
                                    my_gifts.append(gift.id)
                                    res = MyResults(user=request.user.id, board_id=board_id, gifts_id=my_gifts)
                                    res.save()

                        record = GiftWinners(gift_id=ship.gift_id, winner_id=request.user.id)
                        record.save()

                if is_win:
                    context['win'] = win
                    context['action'] = 'Попадание!'
                else:
                    context['action'] = 'Промах(((, не расcтраивайтесь, следующий будет точно в цель'

            context['errors'] = errors
            if acc_obj.shots == 0:
                my_win = []
                results = []
                is_win_something = False
                for res in my_res:
                        if res.board_id == board_id and res.user == request.user.id:
                            results = res.gifts_id
                            is_win_something = True

                for g in gifts:
                    if g.id in results:
                        my_win.append(g)
                if is_win_something:
                    context['results'] = my_win
                errors.append('Выстрелы закончились! Попытайте удачу в другой раз')
                arr = []
                recent_sh.delete()
                for res in my_res:
                    if res.board_id == board_id and res.user == request.user.id:
                        res.delete()
                for id in board.users_id:
                    if id != request.user.id:
                        arr.append(id)
                board.users_id = arr
                acc_obj.delete()
                board.save()

    return render(request, 'user/battle.html', context)


@staff_member_required
def shots(request, board_id):
    context = {}
    errors = []
    board = Board.objects.get(id=board_id)
    users = User.objects.all()
    access = BoardAccess.objects.all()
    acc = []
    for b in access:
        if b.board_id == board_id:
            acc.append(b)
    context['access'] = acc
    context['users'] = users
    context['board'] = board
    if request.method == "POST":
        form = ShotForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            shot_count = form.cleaned_data['shots']
            is_exist = False
            doesnt_exist_yet = True
            for ac in access:
                if ac.board_id == board_id and ac.us == user:
                    doesnt_exist_yet = False
            if not doesnt_exist_yet:
                errors.append('Этот пользователь уже имеет доступ к данному полю')
            for use in users:
                if use.id == user:
                    is_exist = True
            if not is_exist:
                errors.append('Пользователя с таким id не существует в базе данных')
            if len(errors) == 0:
                board.users_id.append(user)
                record = BoardAccess(shots=shot_count, board_id=board_id, us=user, start_shot=shot_count)
                record.save()
                board.save()
            else:
                context['errors'] = errors

    return render(request, 'admin/addshot.html', context)




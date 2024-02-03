from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from polls.models import Gifts, Board, Ship, BoardAccess, MyShots, MyResults, MyGifts
from polls.forms import GiftForm, BoardForm, ShipForm, ShotForm, BattleForm, Filter
from django.contrib.auth.models import User

description = 'Web-игра морской бой. Используйте начисленные Вам выстрелы. При попадании в корабль Вы получаете гарантированный приз.'


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
    acc = BoardAccess.objects.filter(us=request.user.id)
    context['access'] = acc
    for board in boards:
        if request.user.id in board.users_id:
            game_boards.append(board)
    context['boards'] = game_boards
    return render(request, 'user/SeaBattle.html', context)


def mygift_page(request):
    context = {}
    errors = []
    gifts = MyGifts.objects.filter(user=request.user.id)
    if len(gifts) == 0:
        errors.append('У вас нет призов')
        context['errors'] = errors
    context['my_gifts'] = MyGifts.objects.filter(user=request.user.id)
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
    try:
        board = Board.objects.get(id=board_id)
    except:
        return render(request, 'admin/fields.html', context)
    acc = BoardAccess.objects.all()
    is_not_playing = True
    errors = []
    for access in acc:
        if access.board_id == board_id:
            if access.start_shot != access.shots:
                is_not_playing = False
    if not is_not_playing:
        errors.append('Данное поле используется пользователями. Вы сможете его удалить, как только игра будет окончена')
        context['errors'] = errors
    if is_not_playing:
        for access in acc:
            if access.board_id == board_id:
                access.delete()
        for ship in ships:
            if ship.board_id == board_id:
                ship.delete()
        board.delete()
        return redirect('/fields/')
    return render(request, 'admin/fields.html', context)


@staff_member_required
def delete_user_and_shots(request, access_id):
    context = {}
    is_not_playing = True
    errors = []
    acc = BoardAccess.objects.get(id=access_id)
    if acc.start_shot != acc.shots:
        is_not_playing = False
    if not is_not_playing:
        errors.append(
            'Данное поле используется пользователями. Вы сможете его изменить, как только игра будет окончена')
        context['errors'] = errors
    if is_not_playing:
        acc.delete()
        return redirect(f'/add_shots/{acc.board_id}')
    return render(request, 'admin/addshot.html', context)


@staff_member_required
def delete_gift(request, gift_id):
    context = {}
    errors = []
    boards = Board.objects.all()
    is_exist = True
    gift = Gifts.objects.get(id=gift_id)
    for board in boards:
        ships = Ship.objects.filter(board_id=board.id)
        for ship in ships:
            if ship.gift_id == gift_id:
                is_exist = False
    if is_exist:
        gift.delete()
        for ship in ships:
            if ship.gift_id == gift_id:
                ship.delete()
        return redirect('/settingsgift/')
    else:
        errors.append \
            ('Данный приз связан с кораблем, который уже размещён на игровом поле. Вы сможете его удалить, предварительно удалив все корабли связанные с ним')
        context['errors'] = errors
        return render(request, 'admin/settings_gift.html', context)


@staff_member_required
def delete_ship(request, ship_id):
    context = {}
    errors = []
    ship = Ship.objects.get(id=ship_id)
    acc = BoardAccess.objects.filter(board_id=ship.board_id)
    is_not_playing = True
    for access in acc:
        if access.start_shot != access.shots:
            is_not_playing = False
    if not is_not_playing:
        errors.append(
            'Данное поле используется пользователями. Вы сможете его изменить, как только игра будет окончена')
        context['errors'] = errors
    if is_not_playing:
        board_id = ship.board_id
        ship.delete()
        return redirect(f'/add_ship/{board_id}')
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
        errors.append \
            ('Данное поле используется пользователями. Вы сможете его изменить, как только игра будет окончена')

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
                    errors.append(
                        'Корабль с данными координатами уже существует на данном поле, пожалуйста введите другие координаты')
            if len(errors) > 0:
                context['errors'] = errors
            else:
                record = Ship(x=x, y=y, board_id=board_id, gift_id=gift_id)
                record.save()
                context['update'] = True
    return render(request, 'admin/AddShip.html', context)


@staff_member_required
def create_board(request):
    context = {}
    all_users = User.objects.values()
    context['users'] = all_users
    context['description'] = description
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            record = Board(name=name, size=size, users_id=[])
            record.save()
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
        errors.append(
            'На данном поле некоторые игроки начали битву, пока они не доиграют вы не можете ')
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
    context['history'] = Gifts.objects.all()
    return render(request, 'admin/settings_gift.html', context)


@staff_member_required
def edit_gift(request, gift_id):
    context = {}
    gifts = Gifts.objects.all()
    current_gift = Gifts.objects.get(id=gift_id)
    context['current_gift'] = current_gift
    initial_gift = {
        "name": current_gift.name,
        "description": current_gift.description,
        "Img": current_gift.Img
    }
    errors = []
    if request.method == "POST":
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            img = form.cleaned_data['Img']
            for gift in gifts:
                if gift.name == name:
                    errors.append('Приз с данным названием уже существует, пожалуйста введите другое название')
            if len(errors) > 0:
                context['errors'] = errors
            else:
                current_gift.name = name
                current_gift.description = description
                current_gift.Img = img
                current_gift.save()
                return redirect('/settingsgift/')
    else:
        form = GiftForm()
        context['form'] = form

    return render(request, 'admin/edit_gift.html', context)


@staff_member_required
def create_gift(request):
    context = {}
    gifts = Gifts.objects.all()
    errors = []
    if request.method == "POST":
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            img = form.cleaned_data['Img']
            if len(errors) > 0:
                context['errors'] = errors
            else:
                record = Gifts(name=name, description=description, Img=img)
                record.save()
                return redirect('/settingsgift/')
    else:
        form = GiftForm()
        context['form'] = form

    return render(request, 'admin/Creategift.html', context)


def battle_page(request, board_id):
    context = {}

    acc = BoardAccess.objects.all()
    mega_errors = []
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
    context['description'] = description
    board = Board.objects.get(id=board_id)

    tbl = '<table>'
    for i in range(board.size):
        tbl += '<tr>'
        for j in range(board.size):
            tbl += f'<td>{j}</td>'
        tbl += '</tr>'
    tbl += '</table>'
    context['table'] = tbl
    context['a'] = 'a222'

    ships = Ship.objects.filter(board_id=board_id)
    if len(ships) == 0:
        mega_errors.append \
            ('На данном игровом поле нет кораблей, вы сможете начать игру как только администратор их добавит')
        context['mega_errors'] = mega_errors
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
                                record = MyGifts(name=gift.name, description=gift.description, Img=gift.Img,
                                                 user=request.user.id)
                                record.save()
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
                context['update'] = True
            else:
                context['errors'] = errors

    return render(request, 'admin/addshot.html', context)


def field(request):
    context = {}
    array = []
    return render(request, 'field.html', context)


def users_gift(request):
    context = {}
    errors = []
    all_users = User.objects.all()
    if request.method == "POST":
        form = Filter(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            is_exist = False
            for us in all_users:
                if us.username == username:
                    context['gifts'] = MyGifts.objects.filter(user=us.id)
                    context['user'] = username
                    is_exist = True
                    break
            if not is_exist:
                errors.append('Пользователя с данным именем не существует, либо данный пользователь не выйграл ни одного приза')
                context['errors'] = errors
    context['history'] = Gifts.objects.all()
    return render(request, 'admin/users_gift.html', context)

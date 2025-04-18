
from flask import Blueprint, request, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

def init_auth_routes(app, login_manager: LoginManager):
    @login_manager.user_loader
    def load_user(user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT p.userName AS username, p.password AS password, a.roleID AS role '
            'FROM Person p LEFT JOIN Act a ON p.userName = a.userName '
            'WHERE p.userName = %s',
            (user_id,)
        )
        user = cursor.fetchone()
        if user is None:
            return None
        return User(user_id=user['username'], username=user['username'], role=user['role'])

    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        fname = data.get('first_name')
        lname = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        role = data.get('role')

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute('SELECT 1 FROM Person WHERE userName = %s', (username,))
        if cursor.fetchone():
            return jsonify({'error': f"User {username} already exists."}), 400

        cursor.execute('SELECT 1 FROM Role WHERE roleID = %s', (role,))
        if not cursor.fetchone():
            return jsonify({'error': f"Invalid role ID: {role}"}), 400

        try:
            cursor.execute(
                'INSERT INTO Person (userName, password, fname, lname, email) '
                'VALUES (%s, %s, %s, %s, %s)',
                (username, generate_password_hash(password), fname, lname, email)
            )
            cursor.execute(
                'INSERT INTO PersonPhone (userName, phone) VALUES (%s, %s)',
                (username, phone)
            )
            cursor.execute(
                'INSERT INTO Act (userName, roleID) VALUES (%s, %s)',
                (username, role)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500

        return jsonify({'message': 'Registration successful'}), 201

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT p.userName AS username, p.password AS password, a.roleID AS role '
            'FROM Person p LEFT JOIN Act a ON p.userName = a.userName '
            'WHERE p.userName = %s',
            (username,)
        )
        user = cursor.fetchone()

        if user is None or not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid username or password'}), 401

        wrapped_user = User(user_id=user['username'], username=user['username'], role=user['role'])
        login_user(wrapped_user)
        session['user'] = user['username']
        return jsonify({'message': 'Login successful', 'username': user['username'], 'role': user['role']}), 200

    @auth_bp.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        session.clear()
        return jsonify({'message': 'Logout successful'})

    app.register_blueprint(auth_bp)

# TODO: You can continue adding more endpoints below as needed.


@auth_bp.route('/accept_donation', methods=['POST'])
@login_required
def accept_donation():
    if current_user.role != '1':
        return jsonify({'error': 'Only staff can accept donations'}), 403

    try:
        data = request.get_json()
        db = get_db()
        cursor = db.cursor()

        donor_id = data.get('donor_id')
        main_category = data.get('mainCategory')
        sub_category = data.get('subCategory')
        item_description = data.get('item_description')
        photo_filename = data.get('photo_filename')
        material = data.get('material')
        color = data.get('color')
        is_new = int(data.get('is_new', 0))
        has_pieces = int(data.get('has_pieces', 0))
        donation_date = data.get('donation_date')
        pieces = data.get('pieces', [])

        # 验证 donor 是否为注册捐赠者
        cursor.execute(
            'SELECT userName FROM Act WHERE userName = %s AND roleID = "4"',
            (donor_id,)
        )
        donor = cursor.fetchone()
        if not donor:
            return jsonify({'error': 'The specified donor is not registered'}), 400

        # 插入 Item
        cursor.execute(
            '''
            INSERT INTO Item (mainCategory, subCategory, iDescription, photo, color, isNew, hasPieces, material)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (main_category, sub_category, item_description, photo_filename, color, is_new, has_pieces, material)
        )
        item_id = cursor.lastrowid

        cursor.execute(
            'INSERT INTO DonatedBy (ItemID, userName, donateDate) VALUES (%s, %s, %s)',
            (item_id, donor_id, donation_date)
        )

        for i, piece in enumerate(pieces, start=1):
            cursor.execute(
                '''
                INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (
                    item_id, i,
                    piece.get('description'), piece.get('length'), piece.get('width'), piece.get('height'),
                    piece.get('room_num'), piece.get('shelf_num'), piece.get('notes', '')
                )
            )

        db.commit()
        return jsonify({'message': 'Donation recorded successfully'}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@auth_bp.route('/my_orders', methods=['GET'])
@login_required
def my_orders():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    user_role = current_user.role
    user_name = current_user.username
    result = {'role': user_role}  # ✅ 添加 role 字段

    if user_role == '3':  # Client
        cursor.execute(
            '''
            SELECT o.orderID, o.orderDate, o.orderNotes, i.ItemID, i.iDescription, ii.found
            FROM Ordered o
            JOIN ItemIn ii ON o.orderID = ii.orderID
            JOIN Item i ON ii.ItemID = i.ItemID
            WHERE o.client = %s
            ''',
            (user_name,)
        )
        result['orders'] = cursor.fetchall()

    elif user_role == '1':  # Staff
        cursor.execute(
            'SELECT orderID, orderDate, orderNotes FROM Ordered WHERE supervisor = %s',
            (user_name,)
        )
        result['supervise_orders'] = cursor.fetchall()

        cursor.execute(
            '''
            SELECT o.orderID, o.orderDate, o.orderNotes, d.status
            FROM Ordered o JOIN Delivered d ON o.orderID = d.orderID
            WHERE o.supervisor = %s
            ''',
            (user_name,)
        )
        result['deliver_orders'] = cursor.fetchall()

    elif user_role == '2':  # Volunteer
        cursor.execute(
            '''
            SELECT o.orderID, o.orderDate, o.orderNotes, d.date AS deliveryDate, d.status
            FROM Delivered d JOIN Ordered o ON d.orderID = o.orderID
            WHERE d.userName = %s
            ''',
            (user_name,)
        )
        result['orders'] = cursor.fetchall()

    return jsonify(result)


@auth_bp.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    db = get_db()
    cursor = db.cursor()
    role = current_user.role
    username = current_user.username
    status = request.json.get('status')

    if not status:
        return jsonify({'error': 'Missing status'}), 400

    permitted = False

    if role == '1':
        cursor.execute(
            '''
            SELECT 1 FROM Ordered o
            JOIN Delivered d ON o.orderID = d.orderID
            WHERE o.orderID = %s AND o.supervisor = %s
            ''',
            (order_id, username)
        )
        permitted = cursor.fetchone()
    elif role == '2':
        cursor.execute(
            'SELECT 1 FROM Delivered WHERE orderID = %s AND userName = %s',
            (order_id, username)
        )
        permitted = cursor.fetchone()

    if not permitted:
        return jsonify({'error': 'Unauthorized'}), 403

    cursor.execute(
        'UPDATE Delivered SET status = %s WHERE orderID = %s',
        (status, order_id)
    )
    db.commit()
    return jsonify({'message': 'Status updated successfully'})


@auth_bp.route('/assign_delivery', methods=['POST'])
@login_required
def assign_delivery():
    if current_user.role != '1':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    order_id = data.get('orderID')
    client_username = data.get('clientUsername')

    if not order_id or not client_username:
        return jsonify({'error': 'Missing order ID or username'}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        'SELECT * FROM Ordered WHERE orderID = %s AND supervisor = %s',
        (order_id, current_user.username)
    )
    if not cursor.fetchone():
        return jsonify({'error': 'Order not found or unauthorized'}), 400

    cursor.execute('SELECT * FROM Delivered WHERE orderID = %s', (order_id,))
    if cursor.fetchone():
        return jsonify({'error': 'Order already assigned'}), 400

    cursor.execute(
        'INSERT INTO Delivered (orderID, userName, status) VALUES (%s, %s, %s)',
        (order_id, client_username, 'Preparing')
    )
    db.commit()
    return jsonify({'message': 'Delivery assigned successfully'})

@auth_bp.route('/find_single_item', methods=['POST'])
@login_required
def find_single_item():
    try:
        data = request.get_json()
        item_id = data.get('itemID')
        if not item_id:
            return jsonify({'error': 'Missing item ID'}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT p.pieceNum, l.roomNum, l.shelfNum, l.shelfDescription
            FROM Piece p
            JOIN Location l ON p.roomNum = l.roomNum AND p.shelfNum = l.shelfNum
            WHERE p.ItemID = %s
            """,
            (item_id,)
        )
        rows = cursor.fetchall()
        if not rows:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'locations': rows})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@auth_bp.route('/get_main_categories', methods=['GET'])
@login_required
def get_main_categories():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT mainCategory FROM Category")
    results = cursor.fetchall()
    return jsonify([row['mainCategory'] for row in results])


@auth_bp.route('/get_subcategories/<main_category>', methods=['GET'])
@login_required
def get_subcategories(main_category):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT DISTINCT subCategory FROM Category WHERE mainCategory = %s",
        (main_category,)
    )
    rows = cursor.fetchall()
    return jsonify([row['subCategory'] for row in rows])

@auth_bp.route('/find_order_items', methods=['POST'])
@login_required
def find_order_items():
    try:
        data = request.get_json()
        order_id = data.get('orderID')

        if not order_id:
            return jsonify({'error': 'Missing order ID'}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT i.ItemID, i.iDescription AS itemDescription, p.pieceNum,
                   l.roomNum, l.shelfNum, l.shelfDescription
            FROM ItemIn ii
            JOIN Item i ON ii.ItemID = i.ItemID
            LEFT JOIN Piece p ON i.ItemID = p.ItemID
            LEFT JOIN Location l ON p.roomNum = l.roomNum AND p.shelfNum = l.shelfNum
            WHERE ii.orderID = %s
            """,
            (order_id,)
        )
        rows = cursor.fetchall()

        if not rows:
            return jsonify({'error': 'No items found'}), 404

        return jsonify({'items': rows})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/start_order', methods=['POST'])
@login_required
def start_order():
    if current_user.role != '1':  # Only staff
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    client_username = data.get('client_username')
    order_notes = data.get('order_notes', '')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        'SELECT userName FROM Act WHERE userName = %s AND roleID = "3"',
        (client_username,)
    )
    if not cursor.fetchone():
        return jsonify({'error': 'The specified username is not a valid client'}), 400

    cursor.execute(
        'INSERT INTO Ordered (orderDate, orderNotes, supervisor, client) '
        'VALUES (CURDATE(), %s, %s, %s)',
        (order_notes, current_user.username, client_username)
    )
    order_id = cursor.lastrowid
    db.commit()

    session['order_id'] = order_id
    return jsonify({'message': 'Order started successfully', 'order_id': order_id}), 201

@auth_bp.route('/add_to_order', methods=['POST'])
@login_required
def add_to_order():
    if current_user.role != '1':
        return jsonify({'error': 'Only staff can add items to orders'}), 403

    data = request.get_json()
    item_id = data.get('item_id')
    main_cat = data.get('mainCategory')
    sub_cat = data.get('subCategory')

    order_id = session.get('order_id')
    if not order_id:
        return jsonify({'error': 'No active order found'}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            'INSERT INTO ItemIn (ItemID, orderID, found) VALUES (%s, %s, FALSE)',
            (item_id, order_id)
        )
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Item added successfully', 'order_id': order_id}), 201

@auth_bp.route('/prepare_order', methods=['POST'])
@login_required
def prepare_order():
    if current_user.role != '1':
        return jsonify({'error': 'Only staff members can prepare orders'}), 403

    data = request.get_json()
    search_type = data.get('search_type')
    search_value = data.get('search_value')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    items = []

    try:
        if search_type == 'order_number':
            cursor.execute(
                """
                SELECT Item.ItemID, Item.iDescription, Piece.roomNum, Piece.shelfNum, Piece.pNotes
                FROM Item
                JOIN Piece ON Item.ItemID = Piece.ItemID
                WHERE Item.ItemID IN (
                    SELECT ItemID FROM ItemIn WHERE orderID = %s AND found = 0
                )
                """, (search_value,)
            )
            items = cursor.fetchall()

            cursor.execute(
                "UPDATE Piece SET roomNum = 20, shelfNum = 1, pNotes = 'Ready for delivery' "
                "WHERE ItemID IN (SELECT ItemID FROM ItemIn WHERE orderID = %s AND found = 0)",
                (search_value,)
            )
            cursor.execute(
                "UPDATE ItemIn SET found = TRUE WHERE orderID = %s AND found = 0",
                (search_value,)
            )

        elif search_type == 'client_username':
            cursor.execute(
                "SELECT orderID FROM Ordered WHERE client = %s",
                (search_value,)
            )
            orders = cursor.fetchall()
            if not orders:
                return jsonify({'error': 'No orders found for this client'}), 404

            order_ids = [order['orderID'] for order in orders]
            in_clause = ','.join(['%s'] * len(order_ids))

            cursor.execute(
                f"""
                SELECT Item.ItemID, Item.iDescription, Piece.roomNum, Piece.shelfNum, Piece.pNotes
                FROM Item
                JOIN Piece ON Item.ItemID = Piece.ItemID
                WHERE Item.ItemID IN (
                    SELECT ItemID FROM ItemIn WHERE orderID IN ({in_clause}) AND found = 0
                )
                """, tuple(order_ids)
            )
            items = cursor.fetchall()

            cursor.execute(
                f"""
                UPDATE Piece SET roomNum = 20, shelfNum = 1, pNotes = 'Ready for delivery'
                WHERE ItemID IN (
                    SELECT ItemID FROM ItemIn WHERE orderID IN ({in_clause}) AND found = 0
                )
                """, tuple(order_ids)
            )
            cursor.execute(
                f"""
                UPDATE ItemIn SET found = TRUE
                WHERE orderID IN ({in_clause}) AND found = 0
                """, tuple(order_ids)
            )

        db.commit()
        return jsonify({'items': items}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/get_donors', methods=['GET'])
@login_required
def get_donors():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT userName FROM Act WHERE roleID = %s', ('4',))
    donors = [row['userName'] for row in cursor.fetchall()]
    return jsonify(donors)

@auth_bp.route('/get_locations', methods=['GET'])
@login_required
def get_locations():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT roomNum, shelfNum FROM Location')
    return jsonify(cursor.fetchall())

@auth_bp.route('/get_item_ids', methods=['GET'])
@login_required
def get_item_ids():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT ItemID FROM Item")
    results = [row[0] for row in cursor.fetchall()]
    return jsonify(results)

@auth_bp.route('/get_order_ids', methods=['GET'])
@login_required
def get_order_ids():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT orderID FROM Ordered")
    ids = [row[0] for row in cursor.fetchall()]
    return jsonify(ids)

@auth_bp.route('/get_clients', methods=['GET'])
@login_required
def get_clients():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT userName FROM Act WHERE roleID = '3'")  # roleID 3 是 client
    clients = cursor.fetchall()
    return jsonify([c['userName'] for c in clients])

@auth_bp.route('/get_items/<main_category>/<sub_category>', methods=['GET'])
@login_required
def get_items_by_category(main_category, sub_category):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        '''
        SELECT i.ItemID, i.iDescription, i.material, i.color
        FROM Item i
        LEFT JOIN ItemIn ii ON i.ItemID = ii.ItemID
        WHERE i.mainCategory = %s AND i.subCategory = %s
        AND ii.ItemID IS NULL
        ''',
        (main_category, sub_category)
    )
    items = cursor.fetchall()
    return jsonify(items)

@auth_bp.route('/get_current_order_id', methods=['GET'])
@login_required
def get_current_order_id():
    order_id = session.get('order_id')
    return jsonify({'order_id': order_id}) if order_id else jsonify({'order_id': None})

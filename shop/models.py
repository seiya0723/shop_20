from django.db import models
from django.utils import timezone

from django.conf import settings 
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from django.core.exceptions import ValidationError

from django.db.models import Avg

import uuid


class CategoryParent(models.Model):

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="追加日時",default=timezone.now)
    name    = models.CharField(verbose_name="商品カテゴリ名",max_length=100)

    def categories(self):
        return Category.objects.filter(parent=self.id).order_by("-dt")


    #この親カテゴリに所属する全ての商品を表示させる。
    def products(self):
        return Product.objects.filter(category__parent=self.id).order_by("-dt")

    def __str__(self):
        return self.name


class Category(models.Model):

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="追加日時",default=timezone.now)
    parent  = models.ForeignKey(CategoryParent,verbose_name="所属親カテゴリ",on_delete=models.PROTECT)
    name    = models.CharField(verbose_name="商品カテゴリ名",max_length=100)

    #このカテゴリに所属する全ての商品を表示させる。
    def products(self):
        return Product.objects.filter(category=self.id).order_by("-dt")


    def __str__(self):
        return self.name


#商品グループのモデル
class ProductGroup(models.Model):

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name    = models.CharField(verbose_name="商品グループ名",max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    
    #TODO:実践では所属グループ、サイズ、カラー、種類の全てが一致するデータの入力は拒否する( unique_together )
    # https://noauto-nolife.com/post/django-same-user-operate-prevent/

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)

    category    = models.ForeignKey(Category,verbose_name="所属カテゴリ",on_delete=models.PROTECT,null=True,blank=True)
    name        = models.CharField(verbose_name="商品名",max_length=100)
    price       = models.PositiveIntegerField(verbose_name="価格")
    img         = models.ImageField(verbose_name="商品サムネイル画像",upload_to="shop/product/img/")

    #商品の在庫数。(在庫切れでも注文を許すかどうかはsettings.pyなどに書いて分岐させる方式を取る。そのためここはマイナス値を受けるIntegerFieldを使う)
    stock       = models.IntegerField(verbose_name="在庫数",default=0)
    group       = models.ForeignKey(ProductGroup,verbose_name="所属商品グループ",null=True,blank=True,on_delete=models.CASCADE)

    size        = models.CharField(verbose_name="サイズ",choices=settings.SIZE,max_length=2,null=True,blank=True)
    color_regex = RegexValidator(regex=r'^#(?:[0-9a-f]{6})$')
    color       = models.CharField(verbose_name="色",max_length=7,validators=[color_regex],null=True,blank=True)

    #自由記入の種類の指定(服の模様、食品のフレバー、ソフトのエディション等をここに書く)
    kind        = models.CharField(verbose_name="種類",max_length=30,null=True,blank=True)


    #商品に紐付いている画像を出力
    def images(self):
        return ProductImage.objects.filter(product=self.id).order_by("-dt")

    def __str__(self):
        return self.name

    #TODO:全購入履歴を返す(これで、この商品がいつ、どれだけ売れたのかを把握することができる。(ただし、ユーザーモデルと紐付いているので、レンダリング時の書き方によっては誰が何を買ったかが出品者にもわかるかもしれない))
    def order_details(self):

        print("order_details")
        obj = OrderDetail.objects.filter(product=self.id).order_by("-dt")

        initial = OrderDetail()
        print(obj)

        for o in obj:
            o.user  = initial.user
            o.order = initial.order

        print(obj)

        return obj
        #return OrderDetail.objects.filter(product=self.id).order_by("-dt")
    

    #TIPS:実行するメソッドと同一のモデルでも呼び出すことはできる。
    #同じグループの商品を抽出するメソッド。
    def groups(self):
        if self.group:
            return Product.objects.filter(group=self.group.id).order_by("-dt")
        
        return None


    def amount_comments(self):
        return ProductComment.objects.filter(product=self.id).count()


    def avg_star(self):
        product_comment = ProductComment.objects.filter(product=self.id).aggregate(Avg("star"))
        if product_comment["star__avg"]:
            return product_comment["star__avg"]
        else:
            return 0


    def avg_star_few(self):
        product_comment = ProductComment.objects.filter(product=self.id).aggregate(Avg("star"))
        avg             = product_comment["star__avg"]

        #平均スコアなしの場合は0を返す
        if not avg:
            return 0

        #少数指定の場合、小数部を表示(0~0.4は0、0.4~0.6は0.5、0.6~1は1と表現)
        few     = avg - int(avg)

        if 0.4 > few:
            return 0
        elif 0.6 > few:
            return 0.5
        else:
            return 1 


class ProductImage(models.Model):
    
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    product = models.ForeignKey(Product,verbose_name="対象商品",on_delete=models.CASCADE)

    img     = models.ImageField(verbose_name="画像",upload_to="shop/product_image/img/")



bad_words   = [ "あああ","いいい" ]

def validate_bad_word(value):
    for word in bad_words:
        if word in value:
            #TIPS:forループ中でもraise命令で後続の処理は実行されなくなるため、breakは不要
            raise ValidationError( "『"+value+"』には不適切な単語『"+word+"』が含まれています。" )

class ProductComment(models.Model):

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    product = models.ForeignKey(Product,verbose_name="対象商品",on_delete=models.CASCADE)

    star    = models.IntegerField(verbose_name="星",validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.CharField(verbose_name="コメント",max_length=1000, validators=[validate_bad_word])
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成した人", on_delete=models.CASCADE)

    #コメント表示の承認
    approval    = models.BooleanField(verbose_name="承認済み",default=False)


    
class Cart(models.Model):

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="カート追加日時",default=timezone.now)
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="カート所有者", on_delete=models.CASCADE)

    product = models.ForeignKey(Product, verbose_name="商品", on_delete=models.CASCADE)
    amount  = models.IntegerField(verbose_name="商品の個数", default=1, validators=[MinValueValidator(1)] )
    
    def __str__(self):
        return self.product.name

    def total(self):
        return self.product.price * self.amount

    #カートの商品の数量変更を行う時、 [商品の在庫 >= 変更後の数量] の条件に一致しているかをチェックする
    def amount_change(self, after_value):
        if self.product.stock >= after_value:
            return True
        else:
            return False


#住所は複数指定できる。    
class Address(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name="作成日時",default=timezone.now)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="作成した人", on_delete=models.CASCADE)

    prefecture  = models.CharField(verbose_name="都道府県",choices=settings.PREFECTURES,max_length=4)
    city        = models.CharField(verbose_name="市町村",max_length=50)
    address     = models.CharField(verbose_name="番地・部屋番号",max_length=100)



class Order(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name="注文日時",default=timezone.now)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="注文した人", on_delete=models.CASCADE)

    prefecture  = models.CharField(verbose_name="配送先の都道府県",max_length=4)
    city        = models.CharField(verbose_name="配送先の市町村",max_length=50)
    address     = models.CharField(verbose_name="配送先の番地・部屋番号",max_length=100)

    paid        = models.DateTimeField(verbose_name="支払い確認日時",null=True,blank=True)
    deliverd    = models.DateTimeField(verbose_name="配送処理日時",null=True,blank=True)

    #CHECK:テストのセッションIDは66文字のようだが、念の為200文字確保(後に修正する)
    session_id  = models.CharField(verbose_name="セッションID",max_length=200,null=True,blank=True)


    #この注文に所属する注文詳細を表示させる。
    def details(self):
        return OrderDetail.objects.filter(order=self.id, user=self.user.id).order_by("-dt")


class OrderDetail(models.Model):

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt              = models.DateTimeField(verbose_name="登録日時",default=timezone.now)

    #TODO:商品の購入記録などを表示する時、個人情報を秘匿化させるため、nullとblankを許す
    order           = models.ForeignKey(Order, verbose_name="所属する注文", on_delete=models.CASCADE,null=True,blank=True)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="注文した人", on_delete=models.CASCADE,null=True,blank=True)

    #TODO:商品モデルの1対多(購入履歴記録用)。商品が消された時、購入履歴も芋づる式に消えてしまうと、問題ありなのでon_deleteはSET_NULLにする。
    product         = models.ForeignKey(Product,verbose_name="商品",on_delete=models.SET_NULL,null=True,blank=True)

    product_price   = models.PositiveIntegerField(verbose_name="注文時の商品価格")
    product_name    = models.CharField(verbose_name="注文時の商品名",max_length=100)
    amount          = models.IntegerField(verbose_name="注文した商品の個数", default=1, validators=[MinValueValidator(1)] )




class History(models.Model):

    #https://noauto-nolife.com/post/django-same-user-operate-prevent/
    class Meta:
        #商品、日付、ユーザーがそれぞれ一致していなければ保存を許可する。
        unique_together = ("date","user","product")

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    #TIPS:ユニークのバリデーションに失敗してしまうので、日付フィールドにdefaultを指定してはならない。
    #date    = models.DateField(verbose_name="閲覧日",default=timezone.localdate)
    date    = models.DateField(verbose_name="閲覧日")

    user    = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="閲覧した人", on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,verbose_name="閲覧した商品",on_delete=models.SET_NULL,null=True,blank=True)

    #ip          = models.GenericIPAddressField(verbose_name="再生した人のIPアドレス")



#お気に入り
"""
class FavoriteGroup(models.Model):
    pass

class Favorite(models.Model):
    pass
"""


#TODO:追加予定
"""
商品閲覧履歴
商品マイリスト
"""


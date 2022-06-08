from django import forms 

from .models import Cart,Address,Order,OrderDetail,ProductComment,History

class CartForm(forms.ModelForm):

    class Meta:
        model   = Cart
        fields  = [ "user","product","amount" ]

class ProductSortForm(forms.Form):

    #並び替えの選択肢を作る
    choices         = [
                        ("price","価格安い順"),
                        ("-price","価格高い順"),
                    ]

    #並び替えバリデーション用のフィールド
    order_by        = forms.ChoiceField(choices=choices)


class ProductMaxPriceForm(forms.Form):

    max_price       = forms.IntegerField()

class ProductMinPriceForm(forms.Form):

    min_price       = forms.IntegerField()


class ProductCommentForm(forms.ModelForm):

    class Meta:
        model   = ProductComment
        fields  = [ "user","product","star","comment" ]





class AddressForm(forms.ModelForm):
    class Meta:
        model   = Address
        fields  = [ "user","prefecture","city","address" ]


#CheckoutBeforeViewにて指定された住所をOrderモデルへ記録。
class OrderBeforeForm(forms.ModelForm):
    class Meta:
        model   = Order
        fields  = [ "user","prefecture","city","address" ]

#CheckoutViewにて、セッションIDを記録する用
class OrderSessionForm(forms.ModelForm):
    class Meta:
        model   = Order
        fields  = [ "session_id" ]

class OrderCheckoutSuccessForm(forms.ModelForm):
    class Meta:
        model   = Order
        fields  = [ "paid" ]

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model   = OrderDetail
        fields  = [ "order","user","product","product_price","product_name","amount", ]



#年検索をするため、モデルを使用しないフォームクラスを作る
class YearForm(forms.Form):
    year    = forms.IntegerField()


class HistoryForm(forms.ModelForm):

    class Meta:
        model   = History
        #UniqueTogetherを使う時、UniqueTogetherの対象のフィールドを全て下記のfieldsに含めないとDBがエラーを出す。
        fields  = [ "date","user","product" ]




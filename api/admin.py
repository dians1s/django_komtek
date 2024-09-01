from django.contrib import admin
from .models import Guide, GuideVersion, GuideElement
from .forms import GuideVersionForm, GuideElementForm


class GuideVersionInline(admin.TabularInline):
    model = GuideVersion
    fields = ('codeGuide', 'version', 'dateStart')


class GuideElementInline(admin.TabularInline):
    model = GuideElement
    fields = ('elementCode', 'elementValue')


class GuideAdmin(admin.ModelAdmin):
    list_display = ('getId', 'getCode', 'getName',
                    'currentVersion', 'currentDateStart')
    inlines = [GuideVersionInline]
    fields = ('code', 'name', 'description')

    def getId(self, obj):
        return str(obj.id)

    getId.short_description = 'Идентификатор'

    def getCode(self, obj):
        return str(obj.code)

    getCode.short_description = 'Код'

    def getName(self, obj):
        return obj.name

    getName.short_description = 'Наименование'

    def currentVersion(self, obj):
        try:
            latest_version = GuideVersion.objects.filter(
                codeGuide=obj).latest('dateStart')
            return latest_version.version
        except:
            return 'Нет версий'

    currentVersion.short_description = 'Текущая версия'

    def currentDateStart(self, obj):
        try:
            latest_date = GuideVersion.objects.filter(
                codeGuide=obj).latest('dateStart')
            return latest_date.dateStart
        except:
            return 'Нет даты'

    currentDateStart.short_description = 'Дата начала действия версии'


class GuideVersionAdmin(admin.ModelAdmin):
    form = GuideVersionForm
    list_display = ('getcodeGuide', 'getNameGuide',
                    'getVersion', 'getDateStart')
    inlines = [GuideElementInline]
    fields = ('codeGuide', 'version', 'dateStart')

    def getcodeGuide(self, obj):
        return str(obj.codeGuide.code)

    getcodeGuide.short_description = 'Код справочника'

    def getNameGuide(self, obj):
        return Guide.objects.get(code=obj.codeGuide.code).name

    getNameGuide.short_description = 'Наименование справочника'

    def getVersion(self, obj):
        return str(obj.version)

    getVersion.short_description = 'Версия'

    def getDateStart(self, obj):
        return str(obj.dateStart)

    getDateStart.short_description = 'Дата начала версии'


class GuideElementAdmin(admin.ModelAdmin):
    form = GuideElementForm
    list_display = ('getIdVersion', 'getElementCode', 'getElementValue')
    fields = ('idVersion', 'elementCode', 'elementValue')

    def getIdVersion(self, obj):
        return str(obj.idVersion)

    getIdVersion.short_description = 'Идентификатор версии'

    def getElementCode(self, obj):
        return obj.elementCode

    getElementCode.short_description = 'Код элемента'

    def getElementValue(self, obj):
        return obj.elementValue

    getElementValue.short_description = 'Значение элемента'


admin.site.register(Guide, GuideAdmin)
admin.site.register(GuideVersion, GuideVersionAdmin)
admin.site.register(GuideElement, GuideElementAdmin)

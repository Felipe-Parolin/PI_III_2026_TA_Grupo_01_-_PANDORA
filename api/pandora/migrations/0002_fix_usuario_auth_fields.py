from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import migrations, models


def copy_senha_hash_to_password(apps, schema_editor):
    Usuario = apps.get_model("pandora", "Usuario")

    for usuario in Usuario.objects.all().iterator():
        senha_atual = getattr(usuario, "senha_hash", "") or ""

        if not senha_atual:
            usuario.password = ""
            usuario.save(update_fields=["password"])
            continue

        try:
            identify_hasher(senha_atual)
            senha_convertida = senha_atual
        except Exception:
            senha_convertida = make_password(senha_atual)

        usuario.password = senha_convertida
        usuario.save(update_fields=["password"])


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("pandora", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="usuario",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="superuser status",
            ),
        ),
        migrations.AddField(
            model_name="usuario",
            name="last_login",
            field=models.DateTimeField(blank=True, null=True, verbose_name="last login"),
        ),
        migrations.AddField(
            model_name="usuario",
            name="password",
            field=models.CharField(default="", max_length=128, verbose_name="password"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="usuario",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.RunPython(copy_senha_hash_to_password, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="usuario",
            name="senha_hash",
        ),
    ]

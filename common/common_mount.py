mount = Misc.ReadSharedValue("mount")
if mount <= 0:
    mount = Target.PromptTarget("Select your mount")
    Misc.SetSharedValue("mount", mount)

if Player.Mount is not None:
    Mobiles.UseMobile(Player.Serial)
else:
    Mobiles.UseMobile(mount)
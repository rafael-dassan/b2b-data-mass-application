*** Variables ***

##Rating Service##
${ratingServiceCloseButton}     xpath=//android.widget.TextView[@content-desc="Close"]

##Browse Home##
${categoriesView}         id=browseRecyclerView
${tryAgain}               id=browseTryAgain
${categoryRecyclerView}   xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView
${categoryTextCardSufix}  android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView
${categoryTextCardFrame}  android.widget.FrameLayout
${categoryCardImageSufix}  android.widget.FrameLayout/android.widget.ImageView
${categoryImageView}      xpath=(//android.widget.ImageView[@content-desc="Category"])
${homeMenu}               xpath=//android.widget.ImageButton[@content-desc="Menu btn"]
${drawerMenu}             id=com.abinbev.android.tapwiser.southAfrica.debug:id/menu_container
${combosMenu}             xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[2]

##Browse Promotions##
${promotionView}           id=view_pager
${promotion1}              xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.ImageView[1]
${promotion2}              xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.ImageView[2]

##Browse Sub-Categories##
${subCategoriesView}          id=brandsRecyclerView
${subCategoriesCardFrame}     android.widget.LinearLayout
${subCategoriesCardSufix}     android.widget.LinearLayout
${subCategoryRecyclerView}    xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView
${subCategoryTextCardFrame}   android.widget.LinearLayout
${subCategoryTextCardSufix}   android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView
${subCategoryBackButton}      xpath=//android.widget.ImageButton[@content-desc="Back btn"]
${subCategoryImageView}       xpath=(//android.widget.ImageView[@content-desc="Brand"])

##Browse Items##
${categoryView}               xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.support.v7.widget.RecyclerView
${categoryItemsCard1}         xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]
${categoryImage}              id=brand_image
${categoryItemsCloseButton}   xpath=//android.widget.ImageButton[@content-desc="Back btn"]
${categoryItemsRecyclerView}    xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.support.v7.widget.RecyclerView
${categoryItemsTextCardFrame}   android.widget.RelativeLayout
${categoryItemsTextCardSufix}   android.widget.LinearLayout[1]/android.widget.TextView[1]

##Combos##
${combosTable}            id=com.abinbev.android.tapwiser.southAfrica.debug:id/rvCombos
${comboTitlePrefix}             xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout
${comboTitleSufix}              android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[1]
${comboDescriptionPrefix}       xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout
${comboDescriptionSufix}        android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[2]
${comboDiscountedPricePrefix}   xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout
${comboDiscountedPriceSufix}    android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]

### Symbols ###
${slash}                    \/
${leftBrackets}             [
${rightBrackets}            ]
${noCategory}               ${EMPTY}
${noCombo}                  ${EMPTY}